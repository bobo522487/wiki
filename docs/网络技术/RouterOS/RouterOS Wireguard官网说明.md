# 应用实例

## 站点到站点 WireGuard 隧道

考虑如下图所示的设置。两个远程办公室路由器连接到互联网，办公室工作站位于 NAT 后面。每个办公室都有自己的本地子网，Office1 为 10.1.202.0/24，Office2 为 10.1.101.0/24。两个远程办公室都需要在路由器后面建立通往本地网络的安全隧道。

![img](https://help.mikrotik.com/docs/download/attachments/69664792/Site-to-site-ipsec-example.png?version=1&modificationDate=1622538715602&api=v2)

### WireGuard 接口配置

首先，必须在两个站点上配置 WireGuard 接口，以允许自动生成私钥和公钥。两个路由器的命令相同：

```
/interface/wireguard/add listen-port=13231 name=wireguard1
```

现在，当打印接口详细信息时，私钥和公钥都应该可见以允许交换。



远程端设备永远不需要任何私钥 - 因此称为私有。

**办公室1**

```
/interface/wireguard/print
Flags: X - disabled; R - running 0 R name="wireguard1"   mtu=1420   listen-port=13231   private-key="yKt9NJ4e5qlaSgh48WnPCDCEkDmq+VsBTt/DDEBWfEo="   public-key="u7gYAg5tkioJDcm3hyS7pm79eADKPs/ZUGON6/fF3iI="
```

**办公室2**

```
/interface/wireguard/print
Flags: X - disabled; R - running 0 R name="wireguard1"   mtu=1420   listen-port=13231   private-key="KMwxqe/iXAU8Jn9dd1o5pPdHep2blGxNWm9I944/I24="   public-key="v/oIzPyFm1FPHrqhytZgsKjU7mUToQHLrW+Tb5e601M="
```

### 对等配置

对等配置定义谁可以使用 WireGuard 接口以及可以通过它发送什么类型的流量。为了识别远程对等体，必须将其公钥与创建的 WireGuard 接口一起指定。

**办公室1**

```
/interface/wireguard/peers/add allowed-address=10.1.101.0/24   endpoint-address=192.168.80.1   endpoint-port=13231   interface=wireguard1   \public-key="v/oIzPyFm1FPHrqhytZgsKjU7mUToQHLrW+Tb5e601M="
```

**办公室2**

```
/interface/wireguard/peers/add allowed-address=10.1.202.0/24   endpoint-address=192.168.90.1   endpoint-port=13231   interface=wireguard1   \public-key="u7gYAg5tkioJDcm3hyS7pm79eADKPs/ZUGON6/fF3iI="
```

### IP和路由配置

最后，必须配置 IP 和路由信息以允许通过隧道发送流量。

**办公室1**

```
/ip/address/add address=10.255.255.1/30   interface=wireguard1/ip/routeadd dst-address=10.1.101.0/24   gateway=wireguard1
```

**办公室2**

```
/ip/address/add address=10.255.255.2/30   interface=wireguard1/ip/routeadd dst-address=10.1.202.0/24   gateway=wireguard1
```

### 防火墙注意事项

默认的 RouterOS 防火墙将阻止隧道正确建立。在两个站点上执行任何丢弃规则之前，应在“输入”链中接受流量。

**办公室1**

```
/ip/firewall/filter/add action=accept   chain=input   dst-port=13231   protocol=udp   src-address=192.168.80.1
```

**办公室2**

```
/ip/firewall/filter/add action=accept   chain=input   dst-port=13231   protocol=udp   src-address=192.168.90.1
```

此外，“转发”链也可能限制子网之间的通信，因此也应在任何丢弃规则之前接受此类流量。

**办公室1**

```
/ip/firewall/filter/add action=accept   chain=forward   dst-address=10.1.202.0/24   src-address=10.1.101.0/24add action=accept   chain=forward   dst-address=10.1.101.0/24   src-address=10.1.202.0/24
```

**办公室2**

```
/ip/firewall/filter/add action=accept   chain=forward   dst-address=10.1.101.0/24   src-address=10.1.202.0/24add action=accept   chain=forward   dst-address=10.1.202.0/24   src-address=10.1.101.0/24
```

# RoadWarrior WireGuard 隧道

## 路由器操作系统配置

添加新的 WireGuard 接口并为其分配 IP 地址。

```
/interface wireguard add listen-port=13230   name=wireguard_phone
/ip address add address=192.168.100.1/24   interface=wireguard_phone


# 远程设备上配置公钥。要获取公钥值
/interface wireguard peers add allowed-address=192.168.100.2/32 interface=wireguard_phone public-key="eeUEscll0VQOGIcmF9vDHEzX8oeUiXQFIoVxG/JMEQ4="

# 配置防火墙
/ip firewall filter add action=accept   chain=input   comment="allow WireGuard"   dst-port=13231   protocol=udp   place-before=1
/ip firewall filter add action=accept   chain=input   comment="allow WireGuard traffic"   src-address=192.168.100.0/24   place-before=1


```

添加新的 WireGuard 接口将自动生成一对私钥和公钥。您需要在远程设备上配置公钥。要获取公钥值，只需打印出接口详细信息即可。

```
[admin@home] > /interface wireguard print
      name="wireguard_phone" mtu=1420 listen-port=13230 
      private-key="4OibiJsDYkzcCESyjymR+YTG52moUASeMUfuFmlM+Hw=" 
      public-key="P7+6bhaZJfKG5XsYzGm+xnntTo/m1BQaAt9cyEsQ3BY=" 
```

**防火墙注意事项**

如果您配置了默认或严格的防火墙，则需要允许远程设备与您的设备建立 WireGuard 连接。

```

```

要允许远程设备连接到 RouterOS 服务（例如请求 DNS），请在输入链中允许 WireGuard 子网。

```

```

或者只需将 WireGuard 接口添加到“LAN”接口列表中。



## iOS配置

从 App Store 下载 WireGuard 应用程序。打开它并从头开始创建一个新配置。

![img](https://help.mikrotik.com/docs/download/attachments/69664792/IMG_4392.PNG?version=1&modificationDate=1655382066647&api=v2)

首先，为您的连接指定一个“名称”并选择生成密钥对。生成的公钥对于 RouterOS 端的对等配置是必需的。

**![img](https://help.mikrotik.com/docs/download/attachments/69664792/IMG_4393.PNG?version=1&modificationDate=1655382081378&api=v2)
**

在“地址”字段中指定与服务器端配置位于同一子网中的 IP 地址。该地址将用于通信。对于本例，我们在 RouterOS 端使用 192.168.100.1/24，您可以在这里使用 192.168.100.2。

如有必要，配置 DNS 服务器。如果 RouterOS 端的 IP/DNS 部分下的 allowed-remote-requests 设置为 yes，您可以在此处指定远程 WireGuard IP 地址。

**![img](https://help.mikrotik.com/docs/download/attachments/69664792/IMG_4394.PNG?version=1&modificationDate=1655382092515&api=v2)
**

单击“添加对等点”，显示更多参数。

“公钥”值是在 RouterOS 端的 WireGuard 接口上生成的公钥值。

“端点”是 iOS 设备可以通过 Internet 进行通信的 RouterOS 设备的 IP 或 DNS 以及端口号。

“允许的 IP”设置为 0.0.0.0/0 以允许所有流量通过 WireGuard 隧道发送。

![img](https://help.mikrotik.com/docs/download/attachments/69664792/IMG_4396.PNG?version=1&modificationDate=1655382100586&api=v2)

## Windows 10 配置

从 Wireguard 下载 WireGuard 安装程序
以管理员身份运行。

![img](https://help.mikrotik.com/docs/download/attachments/69664792/test.png?version=1&modificationDate=1679667322504&api=v2)

按 Ctrl+n 添加新的空隧道，添加接口名称，公钥应自动生成，将其复制到 RouterOS 对等配置。
添加到服务器配置，完整配置如下所示（将自动生成的私钥保留在 [Interface] 部分中：

呈现代码宏出错: 参数'com.atlassian.confluence.ext.code.render.InvalidValueException'的值无效

```
[界面]
私钥 = your_auto generated_public_key=
地址 = 192.168.100.3/24
DNS = 192.168.100.1

[同行]
公钥 = your_MikroTik_public_KEY=
允许的IP = 0.0.0.0/0
端点 = example.com:13231
```


保存并激活