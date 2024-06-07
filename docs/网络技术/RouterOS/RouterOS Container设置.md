## RouterOS Container设置



```
#启用container，按提示重启或拨电接电
/system/device-mode/update container=yes
#重启后查看状态如下
[admin@MikroTik] > system/device-mode/print
       mode: enterprise
  container: yes
```



```
#创建一个bridge，用于连接docker
/interface bridge add name=bridge1-docker

#定义bridge_iP
/ip address add address=10.10.5.254/24 interface=bridge1-docker network=10.10.5.0
#创建一个虚拟接口给docker使用并定义IP和网关
/interface veth add address=10.10.5.1/24 gateway=10.10.5.254 name=veth1-adg
#将虚拟接口桥接到bridge上
/interface bridge port add bridge=bridge1-docker interface=veth1-adg


#定义docker仓库url，和用户名密码
/container config
set password=tianyingn registry-url=https://registry-1.docker.io tmpdir=sata/images username=你的用户名 password=你的密码
```

接下来创建container容器,在hub.docker.com找到镜像地址





## enable container mode

```
/system/device-mode/update container=yes
```

## Create network

Add veth interface for the container:

```
/interface/veth/add name=veth1 address=172.17.0.2/24 gateway=172.17.0.1
```

Create a bridge for containers and add veth to it:

```
/interface/bridge/add name=containers
/ip/address/add address=172.17.0.1/24 interface=containers
/interface/bridge/port add bridge=containers interface=veth1
```

Setup NAT for outgoing traffic:

```
/ip/firewall/nat/add chain=srcnat action=masquerade src-address=172.17.0.0/24
```

## Add environment variables and mounts (optional)

Create environment variables for container(optional):

```
/container/envs/add name=pihole_envs key=TZ value="Europe/Riga"
/container/envs/add name=pihole_envs key=WEBPASSWORD value="mysecurepassword"
/container/envs/add name=pihole_envs key=DNSMASQ_USER value="root"
```

Define mounts (optional):

```
/container/mounts/add name=etc_pihole src=disk1/etc dst=/etc/pihole
/container/mounts/add name=dnsmasq_pihole src=disk1/etc-dnsmasq.d dst=/etc/dnsmasq.d
```

### a) get an image from an external library

```
/container/config/set registry-url=https://registry-1.docker.io tmpdir=container
```

```
/container/add remote-image=jeessy/ddns-go:latest interface=veth1 root-dir=container/ddns-go logging=yes

```

