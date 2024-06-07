# [RouterOS Wireguard+OSPF Mesh组网](http://www.irouteros.com/?p=3170)

关于Wireguard的Mesh组网问题，Wireguard只是作为隧道连接实现远端的通道，而这个通道我们可以选择其他任何的隧道协议，视乎Wireguard更受欢迎。如何实现Mesh的路径选择和网络动态自愈能力，才是关键，就像无线网络的802.11s，考虑到这个问题整个网络建立在三层路由通信需要实现路径选择和网络自愈能力，自然就想到了使用OSPF建立动态路由。

该实例为了保证网络的冗余，会要求到每个Peer允许相同的IP通过，需要采用多个Wireguard实例，因为单个Wireguard接口实例无法实现多Peer允许相同IP通过，包括OSPF的组播地址（会导致Cryptokey Routing路由冲突，可以参考[Linux下的Wireguard路由配置理解](http://www.irouteros.com/?p=3298)），网络拓扑如下：

![img](http://www.irouteros.com/wp-content/uploads/2023/03/wirgdospf.png)

使用Wireguard建立3台路由器的远端隧道连接，3台通过OSP使用Area0建立路由关系，其中R3路由器发布192.168.10.0/24的LAN网络路由到OSPF。

## 基础网络配置

**R1路由器**
配置IP地址：

```
### 基础网络配置 ###
# R1路由器 配置IP地址：
/ip address add address=192.168.88.30/24 interface=ether1
# 创建2个Wireguard接口，分别对应R2和R3，监听端口分别使用13231和13232
/interface wireguard add listen-port=13231 name=wireguard1-R2
/interface wireguard add listen-port=13232 name=wireguard2-R3

# R2路由器 配置IP地址：
/ip address add address=192.168.88.31/24 interface=ether1
# 创建2个Wireguard接口，分别对应R1和R3，监听端口分别使用13231和13230
/interface wireguard add listen-port=13231 name=wireguard1-R1
/interface wireguard add listen-port=13230 name=wireguard2-R3

# R3路由器 配置IP地址，在R3路由器添加bridge-lan的10.10.10.1：
/ip address add address=192.168.88.32/24 interface=ether1
/ip address add address=10.10.10.1/24 interface=bridge1
# 创建2个Wireguard接口，分别对应R2和R3，监听端口分别使用13231和13232
/interface wireguard add listen-port=13232 name=wireguard1-R1
/interface wireguard add listen-port=13230 name=wireguard2-R2

### Wireguard连接 ###
# 3台路由器的创建两个Wireguard接口，分别和远端的两台连接，组成一个环形网络 ，多接口的wireguard实例才能让peer通过相同的IP段，多点的OSPF组播通信允许224.0.0.5通过才能实现

# R1路由器
/ip address add address=172.16.0.1/30 interface=wireguard1-R2
/ip address add address=172.17.0.1/30 interface=wireguard2-R3
# R2路由器
/ip address add address=172.16.0.2/30 interface=wireguard1-R1
/ip address add address=172.18.0.1/30 interface=wireguard2-R3
# R3路由器
/ip address add address=172.17.0.2/30 interface=wireguard1-R1
/ip address add address=172.18.0.2/30 interface=wireguard2-R2


# R1路由器连接R2和R3路由器，R2连接IP192.168.88.31，指定端口13231和对端的Public key， R3连接192.168.88.32使用13232连接 ，设置相应的allowed-address通过
/interface/wireguard/peers/add allowed-address=172.16.0.0/30,192.168.10.0/24,224.0.0.5/32 comment=R2 endpoint-address=192.168.88.31 endpoint-port=13231 interface=wireguard1-R2 persistent-keepalive=10s public-key="eeUEscll0VQOGIcmF9vDHEzX8oeUiXQFIoVxG/JMEQ4="
/interface/wireguard/peers/add allowed-address=172.17.0.0/30,192.168.10.0/24,224.0.0.5/32 comment=R3 endpoint-address=192.168.88.32 endpoint-port=13232 interface=wireguard2-R3 persistent-keepalive=10s public-key="mtPhuqpAKTjISgHItQsX4J8Eh0xQitx+ANhOszfIrgQ="

# R2路由器连接R1和R3路由器，R1连接IP192.168.88.30，指定端口13231和对端的Public key， R3连接192.168.88.32使用13230连接 ，设置相应的allowed-address通过
/interface/wireguard/peers/add allowed-address=172.16.0.0/30,192.168.10.0/24,224.0.0.5/32 comment=R1 endpoint-address=192.168.99.30 endpoint-port=13231 interface=wireguard1-R1 persistent-keepalive=10s public-key= "x4nugLg1yrJH1rdwuXbI1OO/ih8kAwuA4ez29/iYCyQ="
/interface/wireguard/peers/add allowed-address=172.18.0.0/30,192.168.10.0/24,224.0.0.5/32 comment=R3 endpoint-address=192.168.99.32 endpoint-port=13230 interface=wireguard2-R3 persistent-keepalive=10s public-key= "WpkkCwhtiWIjDITZN2mfe82oEUbdMAU9/70oRoZ2zwQ="

# R3路由器连接R1和R2路由器，R1连接IP192.168.88.30，指定端口13232和对端的Public key， R2连接192.168.88.31使用13230连接 ，设置相应的allowed-address通过
/interface/wireguard/peers/add allowed-address=172.17.0.0/30,192.168.10.0/24,224.0.0.5/32 comment=R1 endpoint-address=192.168.99.30 endpoint-port=13232 interface=wireguard1-R1 persistent-keepalive=10s public-key="CvOoGQqfIh76q9fVf04Km9IJtdqDLOY4Owr0hNj9ow4="
/interface/wireguard/peers/add allowed-address=172.18.0.0/30,192.168.10.0/24,224.0.0.5/32 comment=R2 endpoint-address=192.168.99.31 endpoint-port=13230 interface=wireguard2-R2 persistent-keepalive=10s public-key= "9Sm+3ZoJZ/ixPk7RY7dtkDM4dWRXaNu7rLjx/HvEmV4="

### OSPF配置 ###
## R1路由器 
# 创建ospf实例，设置area区域0
/routing ospf instance add disabled=no name=ospf-instance-1 redistribute=static
/routing ospf area add disabled=no instance=ospf-instance-1 name=ospf-area-0
# R1与R2和R3建立OSPF关系
/routing ospf interface-template add area=ospf-area-0 disabled=no networks=172.16.0.0/30 type=ptp
/routing ospf interface-template add area=ospf-area-0 disabled=no networks=172.17.0.0/30 type=ptp

## R2路由器 
# 创建ospf实例，设置area区域0
/routing ospf instance add disabled=no name=ospf-instance-1
/routing ospf area add disabled=no instance=ospf-instance-1 name=ospf-area-0
# R2与R1和R3建立OSPF关系
/routing ospf interface-template add area=ospf-area-0 disabled=no networks=172.16.0.0/30 type=ptp
/routing ospf interface-template add area=ospf-area-0 disabled=no networks=172.18.0.0/30 type=ptp

## R3路由器 
# 创建ospf实例，设置area区域0
/routing ospf instance add disabled=no name=ospf-instance-1
/routing ospf area add disabled=no instance=ospf-instance-1 name=ospf-area-1
# R3与R1和R2建立OSPF关系
/routing ospf interface-template add area=ospf-area-1 disabled=no networks=172.18.0.0/30 type=ptp
/routing ospf interface-template add area=ospf-area-1 disabled=no networks=172.17.0.0/30 type=ptp
/routing ospf interface-template add area=ospf-area-1 disabled=no networks=10.10.10.0/24

```



## 

## OSPF配置

查看R3的OSPF邻居关系，到R1和R2的state状态为Full，查看R1和R2的OSPF状态这里不再展示。

```
/routing/ospf/neighbor print
Flags: V - virtual; D - dynamic
0 D instance=ospf-instance-1 area=ospf-area-1 address=172.17.0.1 router-id=172.17.0.1 state="Full" state-changes=4 adjacency=32m11s
timeout=39s

1 D instance=ospf-instance-1 area=ospf-area-1 address=172.18.0.1
router-id=172.18.0.1 state="Full" state-changes=5 adjacency=34m21s
timeout=39s
[admin@R3] /routing/ospf/neighbor>
```

查看R1的路由，可以看到192.168.10.0/24路由来至172.17.0.2%wireguard2-R3，当前R1到R3是直接连接。

```
[admin@R1] /ip/route> print
Flags: D - DYNAMIC; A - ACTIVE; c, o, d, y - COPY; + - ECMP
Columns: DST-ADDRESS, GATEWAY, DISTANCE
DST-ADDRESS GATEWAY DISTANCE
DAd 0.0.0.0/0 192.168.88.1 1
DAc 172.16.0.0/30 wireguard1-R2 0
DAc 172.17.0.0/30 wireguard2-R3 0
DAo+ 172.18.0.0/30 172.16.0.2%wireguard1-R2 110
DAo+ 172.18.0.0/30 172.17.0.2%wireguard2-R3 110
DAo 192.168.10.0/24 172.17.0.2%wireguard2-R3 110
DAc 192.168.88.0/24 ether1 0
```

查看R2的路由

```
[admin@R2] /routing/ospf> /ip route print
Flags: D - DYNAMIC; A - ACTIVE; c, o, d, y - COPY; + - ECMP
Columns: DST-ADDRESS, GATEWAY, DISTANCE
DST-ADDRESS GATEWAY DISTANCE
DAd 0.0.0.0/0 192.168.88.1 1
DAc 172.16.0.0/30 wireguard1-R1 0
DAo+ 172.17.0.0/30 172.16.0.1%wireguard1-R1 110
DAo+ 172.17.0.0/30 172.18.0.2%wireguard2-R3 110
DAc 172.18.0.0/30 wireguard2-R3 0
DAo 192.168.10.0/24 172.18.0.2%wireguard2-R3 110
DAc 192.168.88.0/24 ether1 0
```

中断R3到R1的wireguard连接，R3和R1之间的OSPF中断，OSPF发布的路由将从R3->R2->R1,可以查看R1的路由表，到192.168.10.0/24的路由来至172.16.0.2%wireguard1-R2，R1到192.168.10.0/24路由自动切换到R1->R2->R3。

```
[admin@R1] /interface/wireguard> /ip route/print
Flags: D - DYNAMIC; A - ACTIVE; c, o, d, y - COPY
Columns: DST-ADDRESS, GATEWAY, DISTANCE
DST-ADDRESS GATEWAY DISTANCE
DAd 0.0.0.0/0 192.168.88.1 1
DAc 172.16.0.0/30 wireguard1-R2 0
DAc 172.17.0.0/30 wireguard2-R3 0
DAo 172.18.0.0/30 172.16.0.2%wireguard1-R2 110
DAo 192.168.10.0/24 172.16.0.2%wireguard1-R2 110
DAc 192.168.88.0/24 ether1 0
```

从R3发布的路由R1和R2都能学习到，即使R1到R3路由中断，R1也能从R2学习到R3发布的192.168.10.0/24的路由，这样在基于Wireguard组建的Mesh网络中，使用OSPF实现了网络自愈能力。

选择静态路由也可以实现，R1到R3的192.168.10.0/24需配置两条静态路由，一条经过R2到R3，一条直接到R3，同时R2还要配置静态路由，然后通过distance来控制距离，还需要通过网络监控判断线路是否中断，整个一套配置很繁琐复杂，使用OSPF简化了很多配置。

整套配置思路如果你能理解，放在Openwrt或者其他Linux上，结合OSPF路由协议，也能按照这个方式部署，并不是一定局限于RouterOS平台，只是RouterOS在配置的UI方面要胜过Openwrt和其他Linux。RouterOS逐步完善Container后，在可玩性方面也开始赶上Openwrt。