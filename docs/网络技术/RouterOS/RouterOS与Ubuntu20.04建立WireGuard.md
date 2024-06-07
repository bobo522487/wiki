# [RouterOS与Ubuntu20.04建立WireGuard](http://www.irouteros.com/?p=2622)



考虑这样一个网络情况，当两个异地办公区，officeA和officeB需要建立WireGuard隧道，officeA是RouterOS，而officeB是普通路由器，受限于普通路由器不支持WireGuard协议，无法建立互联，但officeB可以搭建VM虚拟机搭建一台ubuntu20.04服务器，这样可以通过ubuntu20.04与RouterOS建立WireGuard的互联，如下拓扑：

![img](http://www.irouteros.com/wp-content/uploads/2022/04/wg5.png)

在这个拓扑上可以看到，RB5009和Ubuntu20.04建立WireGuard隧道，在ubuntu下有一个独立的网络192.168.50.0/24与OfficeA的192.168.88.0/24做路由互联访问。

### RB5009配置

基于RouterOS的RB5009，能获取公网IP地址上网，具体网络接入配置在此省略，直接介绍配置wireguard，首先在wireguard下新建一个接口wireguard1，如下：

![img](http://www.irouteros.com/wp-content/uploads/2022/04/wg1.png)

记录下RouterOS上wireguard1接口的Public Key，需要在ubuntu配置时添加。

RouterOS在wireguard的peer添加ubuntu的客户端连接参数（Public Key是已经获取，在后面对ubuntu配置的介绍会有），由于ubuntu是在officeB的内网，所以无需指定endpoint的地址。

![img](http://www.irouteros.com/wp-content/uploads/2022/04/wg2.png)

进入/ip address，添加wireguard1接口IP地址10.0.0.1/24，winbox配置如下：

![img](http://www.irouteros.com/wp-content/uploads/2022/04/wg3.png)

在/ip route下添加到目标IP地址段192.168.50.0/24的静态路由，winbox配置如下：

![img](http://www.irouteros.com/wp-content/uploads/2022/04/wg4.png)

### Ubuntu 20.04配置

首先通过apt-get更新镜像库，并安装wireguard，操作如下：

```
apt-get update 
apt-get install wireguard
```

安装完成后，ubuntu生成wireguard的私钥和公钥，并存放在指定目录下

```
wg genkey | tee /etc/wireguard/privatekey | wg pubkey | tee /etc/wireguard/publickey
```

在/etc/wireguard/publickey下查看生成的Public Key，用于添加到RouterOS的wireguard1的Peer配置，之前在RouterOS配置提到。

```
cat /etc/wireguard/publickey
```

同样查看privatekey，用于参数配置

```
cat /etc/wireguard/ privatekey
```

在/etc/wireguard/，通过vi创建配置文件wg0.conf

```
vi /etc/wireguard/wg0.conf
```

添加以下内容，

- Interface接口参数，服务端口是13233,接口IP地址是0.0.2/24，并设置Ubuntu自己的privatekey
- Peer为对端参数：PublicKey填写RouterOS publickey，AllowedIPs填写需要通过所有IP地址，Endpoint设置RouterOS的公网IP地址（假设为88.88.88），端口为13233，设置PersistentKeepalive为25秒（用于存活探测）

```
[Interface]
ListenPort = 13233
Address = 10.0.0.2/24
PrivateKey = 复制Ubuntu privatekey

[Peer]
PublicKey = 复制RouterOS publickey
AllowedIPs = 0.0.0.0/0
Endpoint = 88.88.88.88:13233
PersistentKeepalive = 25
```

然后修改配置文件和key的权限

```
chmod 600 /etc/wireguard/{privatekey,wg0.conf}
```

这个时候如果ubuntu作为路由接入其他网络，需开启Linux的ip forward转发功能，通vi编辑**/etc/sysctl.conf****，**找到这一行 #net.ipv4.ip_forward = 1 去掉注释符 “#” 修改为

```
net.ipv4.ip_forward = 1
```

退出vi编辑，立即生效指令如下，

```
sysctl -p
```

通过命令启用wg0接口

```
root@yus:~# wg-quick up wg0
[#] ip link add wg0 type wireguard
[#] wg setconf wg0 /dev/fd/63
[#] ip -4 address add 10.0.0.2 dev wg0
[#] ip link set mtu 1420 up dev wg0
[#] wg set wg0 fwmark 51820
[#] ip -4 route add 0.0.0.0/0 dev wg0 table 51820
[#] ip -4 rule add not fwmark 51820 table 51820
[#] ip -4 rule add table main suppress_prefixlength 0
[#] sysctl -q net.ipv4.conf.all.src_valid_mark=1
[#] iptables-restore -n
```

注意当AllowedIPs是0.0.0.0/0时，Linux会自动创建一个路由表，生成策略路由，如果你配置主机IP和ubuntu不在同一网段，会造成路由中断，切记考虑你连接ubuntu的IP配置

通过wg命令查看连接状态

```
root@yus:~# wg
interface: wg0
public key: OlczskR4y1Txxxxxxxm37gOo5LoCjhHr1u0VUDzY=
private key: (hidden)
listening port: 13233
fwmark: 0xca6c
peer: kwHdyhZkxxxxxPHDvMRrsgpHs=
endpoint: 88.88.88.88:13233
allowed ips: 0.0.0.0/0
latest handshake: 1 minute, 47 seconds ago
transfer: 10.95 KiB received, 11.41 KiB sent
persistent keepalive: every 25 seconds
```

如果不希望允许所有IP通过，可以这样修改配置文件

```
[Interface]
ListenPort = 13233
Address = 10.0.0.2/24
PrivateKey = privatekey

[Peer]
PublicKey = publickey
AllowedIPs = 10.0.0.0/24,192.168.88.0/24
Endpoint = 88.88.88.88:13233
PersistentKeepalive = 25
```

修改AllowedIPs后，使用以下命令关闭wg0接口

```
wg-quick down wg0
```

再次启用网卡时，可以看到通过ip -4 route add添加了静态路由

```
root@yus:~# wg-quick up wg0
[#] ip link add wg0 type wireguard
[#] wg setconf wg0 /dev/fd/63
[#] ip -4 address add 10.0.0.2/24 dev wg0
[#] ip link set mtu 1420 up dev wg0
[#] ip -4 route add 192.168.88.0/24 dev wg0
```

查看路由，可以看到wireguard自动添加了静态路由：

```
root@yus:~# ip route 
default via 192.168.10.1 dev ens160 proto static
10.0.0.0/24 dev wg0 proto kernel scope link src 10.0.0.2 
192.168.10.0/24 dev ens160 proto kernel scope link src 192.168.10.10
192.168.50.0/24 dev ens192 proto kernel scope link src 
192.168.50.11192.168.88.0/24 dev wg0 scope link
```

这样RB5009和ubuntu的wireguard隧道建立，可以测试192.168.88.0/24到192.168.50.0/24路由是否连通。

提醒：192.168.50.0/24网络是ubuntu的ens192网卡下，ens160接入的是实际的普通路由器192.168.10.0/24局域网，如果希望192.168.10.0/24能访问到RB的192.168.88.0/24网络，需要在普通路由器配置静态路由指向ubuntu的ens160的接口IP，如果是华为路由器配置如下：

```
[HuaWei]ip route-static 192.168.88.0 24 192.168.10.10
```

**RouterOS也需要补充配置**

在peer上增加允许IP地址段192.168.10.0/24，如果你是0.0.0.0/0则无需做配置

![img](http://www.irouteros.com/wp-content/uploads/2022/04/wg6.png)

需要在ip route下添加到192.168.10.0/24经过10.0.0.2的静态路由：

![img](http://www.irouteros.com/wp-content/uploads/2022/04/wg7.png)

注意：以上配置采用静态路由方式，不考虑nat规则，如果你在ubuntu或者routeros配置了nat规则，需要注意接口出方向被转为接口IP地址的情况，这里不做讨论。