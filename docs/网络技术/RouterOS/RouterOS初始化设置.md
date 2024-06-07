## RouterOS初始化设置

```bash
# 时区
/system/clock set time-zone-name=Asia/Shanghai

# 安全性设置
/ip/service set api disabled=yes 
/ip/service set api-ssl disabled=yes 
/ip/service set ftp disabled=yes 
/ip/service set ssh disabled=yes 
/ip/service set telnet disabled=yes 
/ip/service set www disabled=yes 

# 添加网桥bridge1
/interface bridge add auto-mac=yes comment="defconf: Local Bridge" name=bridge1 igmp-snooping=yes dhcp-snooping=yes igmp-version=3

# 网桥IPv4地址
/ip address add address="10.10.10.1/24" interface=bridge1 comment="defconf: Local LAN IPv4 Address"

# 网口备注
/interface set ether1 comment="defconf: Local LAN1"
/interface set ether2 comment="defconf: Local LAN2"
/interface set ether3 comment="defconf: Local LAN3"
/interface set ether4 comment="defconf: Local LAN4"
/interface set ether5 comment="defconf: Local LAN5"
/interface set ether6 comment="defconf: Local IPTV"
/interface set ether7 comment="defconf: Local WAN"

# 将所有 LAN 口都添加入该网桥
/interface bridge port
add bridge=bridge1 interface=ether1
add bridge=bridge1 interface=ether2
add bridge=bridge1 interface=ether3
add bridge=bridge1 interface=ether4
add bridge=bridge1 interface=ether5
add bridge=bridge1 interface=ether6

# 创建 PPPoE 客户端
/interface pppoe-client add name=pppoe-out1 interface=ether7 user=085150736047 password=736047 use-peer-dns=yes add-default-route=yes disabled=no

# 定义 PPPoE 接口组
/interface list
add name=WAN comment="defconf: Connect To Global"
add name=LAN comment="defconf: Local Bridge"
add name=ONU comment="onuconf: Access To ONU"
add name=IPTV comment="onuconf: Access To IPTV"

/interface list member
add interface=pppoe-out1 list=WAN comment="defconf: Connect To Global"
add interface=bridge1 list=LAN comment="defconf: Local Bridge"
add interface=ether7 list=ONU comment="onuconf: Access To ONU"
add interface=ether6 list=IPTV comment="onuconf: Access To IPTV"

# 设置DNS
/ip/dns/set servers=223.5.5.5,114.114.114.114 allow-remote-requests=yes 

# 设置DHCP pool
/ip/pool/add name=Local_Pool_IPv4 ranges=10.10.10.50-10.10.10.250 comment="defconf: Local LAN IPv4 Pool"

# 设置DHCP Server
/ip/dhcp-server/add name=Local_DHCP_IPv4 interface=bridge1 lease-time="1d 00:00:00" address-pool=Local_Pool_IPv4 comment="defconf: Local LAN IPv4 DHCP Server"
/ip/dhcp-server/network/add address=10.10.10.0/24 netmask=24 gateway=10.10.10.1 dns-server=10.10.10.1 ntp-server=10.10.10.1 comment="defconf: Local LAN IPv4 DHCP Network"

#设置NTP Client
/system/ntp/client/set enabled=yes mode=unicast servers=cn.pool.ntp.org vrf=main 

#设置NTP Server
/system/ntp/server/set enabled=yes broadcast=yes broadcast-addresses=10.10.10.1 vrf=main 

#设置NAT
/ip firewall nat add action=masquerade chain=srcnat comment="defconf: masquerade IPv4" out-interface-list=WAN

```



## IPv6设置

```bash
/ipv6/settings/set disable-ipv6=no
/ipv6/dhcp-client/add interface=pppoe-out1 request=prefix pool-name=Local_Pool_GUA_IPv6 pool-prefix-length=64 use-peer-dns=yes add-default-route=no comment="defconf: DHCPv6 on PPPoE"  
/ipv6/address/add address=::1/64 from-pool=Local_Pool_GUA_IPv6 interface=bridge1 advertise=yes comment="defconf: Local LAN GUA IPv6 Address"
# 设置IPv6池
/ipv6/pool/add name=Local_Pool_ULA_IPv6 prefix=fdac::/64 prefix-length=64
/ipv6/address/add address=::1/64 from-pool=Local_Pool_ULA_IPv6 interface=bridge1 advertise=yes comment="defconf: Local LAN ULA IPv6 Address"
/ipv6/address/add address=fdac::1/64 interface=bridge1 advertise=yes comment="defconf: Local LAN ULA IPv6 Address"

# 设置ND服务
/ipv6/nd/prefix/default/set valid-lifetime=02:00:00 preferred-lifetime=01:00:00
/ipv6/nd disable numbers=0
/ipv6/nd/add interface=bridge1 ra-interval=60-120 hop-limit=64 dns=fdac::1 advertise-mac-address=yes advertise-dns=yes

```



## ddns设置

新建System/Scripts，name: ddnsv6

```
##########################################
## RouterOS DDNS 脚本 for 阿里云 / 腾讯云 IPv6版
##
## 该 DDNS 脚本可自动 获取/识别/更新 IP 地址
## 兼容 阿里云 / 腾讯云 DNS接口
##
## 作者: vibbow
## https://vsean.net/
##
## 修改日期: 2023/3/15
##########################################

# 域名
:local domainName "ros.t-plus.com.cn";
# wan接口名称
:local wanInterface "bridge1";
# 要使用的服务 (aliyun/dnspod)
:local service "aliyun";
# API接口 Access ID
:local accessID "LTAI5tCfeuau6HYNJoXGbW5h";
# API接口 Access Secret
:local accessSecret "ojdzwQWEeAGYAWOcCvWjcqdzgXqsrv";

# 腾讯云 (dnspod) 设置
#
# 一般情况下无需设置此内容
# 服务器会自动识别 domainID 和 recordID
#
# 如一直提示 "当前域名无权限，请返回域名列表。"
# 则需要手动设置
:local domainID "";
:local recordID "";

# ==== 以下内容无需修改 ====
# =========================

:local publicIP;
:local dnsIP;
:local epicFail false;

# 获取当前接口IPv6地址
:do {
  :local interfaceIP [ /ipv6 address get [ :pick [ find interface=$wanInterface global ] 0 ] address ]
  :set $interfaceIP [ :pick $interfaceIP 0 [ :find $interfaceIP "/" ] ];

  :set $publicIP [ :toip6 $interfaceIP ];
} \
on-error {
  :set $epicFail true;
  :log error ("DDNSv6: Get public IP failed.");
}

# 获取当前解析的IP
:do {
  :set $dnsIP [ :resolve $domainName ];
} \
on-error {
  :set $epicFail true;
  :log error ("DDNSv6: Resolve domain " . $domainName . " failed.");
}

# 如IP有变动，则更新解析
:if ($epicFail = false && $publicIP != $dnsIP) \
do={
    :local callUrl ("https://ddns6.vsean.net/ddns.php");
    :local postData ("service=" . $service . "&domain=" . $domainName . "&access_id=" . $accessID . "&access_secret=" . $accessSecret . "&domain_id=" . $domainID . "&record_id=" . $recordID);
    :local fetchResult [/tool fetch url=$callUrl mode=https http-method=post http-data=$postData as-value output=user];
    :log info ("DDNSv6: " . $fetchResult->"data");
}

```

打开并修改 PPP/Profiles/default，在Scripts  /  on up里添加 ddnsv6



## WireGuard隧道设置

手机隧道设置：

```
/interface wireguard add listen-port=13230   name=wireguard_phone
/ip address add address=192.168.100.1/24   interface=wireguard_phone


# 远程设备上配置公钥。要获取公钥值
/interface wireguard peers add allowed-address=192.168.100.2/32 interface=wireguard_phone public-key="eeUEscll0VQOGIcmF9vDHEzX8oeUiXQFIoVxG/JMEQ4="

# 配置防火墙
/ip firewall filter add action=accept   chain=input   comment="allow WireGuard"   dst-port=13231   protocol=udp   place-before=1
/ip firewall filter add action=accept   chain=input   comment="allow WireGuard traffic"   src-address=192.168.100.0/24   place-before=1


```



















```


# 设置IPv4 防火墙
/ip firewall address-list
add address=10.10.10.8 comment="onuconf: local ONU address" list=local_onu_ipv4
add address=10.10.10.0/24 comment="lanconf: local LAN address" list=local_lan_ipv4
add address=10.10.10.2 comment="lanconf: local DNS server" list=local_dns_ipv4
add address=0.0.0.0/8 comment="defconf: RFC6890" list=no_forward_ipv4
add address=169.254.0.0/16 comment="defconf: RFC6890" list=no_forward_ipv4
add address=224.0.0.0/4 comment="defconf: multicast" list=no_forward_ipv4
add address=255.255.255.255/32 comment="defconf: RFC6890" list=no_forward_ipv4
add address=127.0.0.0/8 comment="defconf: RFC6890" list=bad_ipv4
add address=192.0.0.0/24 comment="defconf: RFC6890" list=bad_ipv4
add address=192.0.2.0/24 comment="defconf: RFC6890 documentation" list=bad_ipv4
add address=198.51.100.0/24 comment="defconf: RFC6890 documentation" list=bad_ipv4
add address=203.0.113.0/24 comment="defconf: RFC6890 documentation" list=bad_ipv4
add address=240.0.0.0/4 comment="defconf: RFC6890 reserved" list=bad_ipv4
add address=0.0.0.0/8 comment="defconf: RFC6890" list=not_global_ipv4
add address=10.0.0.0/8 comment="defconf: RFC6890" list=not_global_ipv4
add address=100.64.0.0/10 comment="defconf: RFC6890" list=not_global_ipv4
add address=169.254.0.0/16 comment="defconf: RFC6890" list=not_global_ipv4
add address=172.16.0.0/12 comment="defconf: RFC6890" list=not_global_ipv4
add address=192.0.0.0/29 comment="defconf: RFC6890" list=not_global_ipv4
add address=192.168.0.0/16 comment="defconf: RFC6890" list=not_global_ipv4
add address=198.18.0.0/15 comment="defconf: RFC6890 benchmark" list=not_global_ipv4
add address=255.255.255.255/32 comment="defconf: RFC6890" list=not_global_ipv4
add address=224.0.0.0/4 comment="defconf: multicast" list=bad_src_ipv4
add address=255.255.255.255/32 comment="defconf: RFC6890" list=bad_src_ipv4
add address=0.0.0.0/8 comment="defconf: RFC6890" list=bad_dst_ipv4
add address=224.0.0.0/4 comment="defconf: RFC6890" list=bad_dst_ipv4
add comment="ddosconf: DDoS" list=ddos_targets_ipv4
add comment="ddosconf: DDoS" list=ddos_attackers_ipv4

/ip firewall filter
add action=accept chain=input comment="defconf: accept ICMP after RAW" protocol=icmp
add action=accept chain=input comment="defconf: accept established,related,untracked" connection-state=established,related,untracked
add action=drop chain=input comment="defconf: drop invalid" connection-state=invalid
add action=drop chain=input comment="defconf: drop all not coming from LAN" in-interface-list=!LAN
add action=fasttrack-connection chain=forward comment="defconf: fasttrack" connection-state=established,related disabled=yes
add action=accept chain=forward comment="defconf: accept established,related,untracked" connection-state=established,related,untracked
add action=drop chain=forward comment="defconf: drop invalid" connection-state=invalid
add action=drop chain=forward comment="defconf: drop all from WAN not DSTNATed" connection-nat-state=!dstnat connection-state=new in-interface-list=WAN log=yes log-prefix=fw_wan_not_DSTNATed
add action=drop chain=forward comment="onuconf: drop all from ONU not DSTNATed" connection-nat-state=!dstnat connection-state=new in-interface-list=ONU log=yes log-prefix=fw_onu_not_DSTNATed
add action=drop chain=forward comment="defconf: drop bad forward IPs" src-address-list=no_forward_ipv4
add action=drop chain=forward comment="defconf: drop bad forward IPs" dst-address-list=no_forward_ipv4
add action=jump chain=forward comment="ddosconf: DDoS" connection-state=new jump-target=detect_ddos
add action=return chain=detect_ddos comment="ddosconf: DDoS SYN-ACK Flood" dst-limit=32,32,src-and-dst-addresses/10s protocol=tcp tcp-flags=syn,ack log=yes log-prefix=fw_syn_ack_detected
add action=return chain=detect_ddos comment="ddosconf: DDoS" dst-limit=256,32,src-and-dst-addresses/10s
add action=add-dst-to-address-list chain=detect_ddos comment="ddosconf: DDoS" address-list=ddos_targets_ipv4 address-list-timeout=10m
add action=add-src-to-address-list chain=detect_ddos comment="ddosconf: DDoS" address-list=ddos_attackers_ipv4 address-list-timeout=10m log=yes log-prefix=fw_ddos_attackers


/ip firewall nat
add action=masquerade chain=srcnat comment="defconf: masquerade IPv4" out-interface-list=WAN
add action=masquerade chain=srcnat comment="onuconf: access to ONU" out-interface-list=ONU src-address-list=local_lan_ipv4 dst-address-list=local_onu_ipv4
add action=accept chain=dstnat comment="lanconf: accept local DNS server's query (UDP)" dst-port=53 in-interface-list=LAN protocol=udp src-address-list=local_dns_ipv4
add action=accept chain=dstnat comment="lanconf: accept local DNS server's query (TCP)" dst-port=53 in-interface-list=LAN protocol=tcp src-address-list=local_dns_ipv4 log=yes log-prefix=fw_dnsv4_tcp
add action=redirect chain=dstnat comment="lanconf: redirect DNS query (UDP)" dst-port=53 in-interface-list=LAN protocol=udp to-ports=53
add action=redirect chain=dstnat comment="lanconf: redirect DNS query (TCP)" dst-port=53 in-interface-list=LAN protocol=tcp to-ports=53 log=yes log-prefix=fw_dnsv4_tcp


/ip firewall mangle
add action=change-mss chain=forward comment="defconf: fix IPv4 mss For WAN" new-mss=clamp-to-pmtu passthrough=yes protocol=tcp tcp-flags=syn
add action=accept chain=prerouting comment="onuconf: access to ONU" src-address-list=local_lan_ipv4 dst-address-list=local_onu_ipv4


/ip firewall raw
add action=accept chain=prerouting comment="defconf: enable for transparent firewall" disabled=yes
add action=drop chain=prerouting comment="ddosconf: DDoS" dst-address-list=ddos_targets_ipv4 src-address-list=ddos_attackers_ipv4
add action=accept chain=prerouting comment="defconf: accept DHCP discover" dst-address=255.255.255.255 dst-port=67 in-interface-list=LAN protocol=udp src-address=0.0.0.0 src-port=68
add action=drop chain=prerouting comment="defconf: drop bogon IPs" src-address-list=bad_ipv4
add action=drop chain=prerouting comment="defconf: drop bogon IPs" dst-address-list=bad_ipv4
add action=drop chain=prerouting comment="defconf: drop bogon IPs" src-address-list=bad_src_ipv4
add action=drop chain=prerouting comment="defconf: drop bogon IPs" dst-address-list=bad_dst_ipv4
add action=drop chain=prerouting comment="defconf: drop non global from WAN" src-address-list=not_global_ipv4 in-interface-list=WAN
add action=drop chain=prerouting comment="defconf: drop forward to local LAN from WAN" in-interface-list=WAN dst-address-list=local_lan_ipv4 log=yes log-prefix=fw_wan_to_lan_forward
add action=drop chain=prerouting comment="onuconf: drop if not from ONU address" in-interface-list=ONU src-address-list=!local_onu_ipv4 log=yes log-prefix=fw_not_from_onu_address
add action=drop chain=prerouting comment="onuconf: drop forward to local LAN from ONU" in-interface-list=ONU dst-address-list=local_lan_ipv4 log=yes log-prefix=fw_onu_to_lan_forward
add action=drop chain=prerouting comment="defconf: drop local if not from default IP range" in-interface-list=LAN src-address-list=!local_lan_ipv4
add action=drop chain=prerouting comment="defconf: drop bad UDP" port=0 protocol=udp log=yes log-prefix=fw_udp_0_port
add action=jump chain=prerouting comment="defconf: jump to ICMP chain" jump-target=icmp4 protocol=icmp
add action=jump chain=prerouting comment="defconf: jump to TCP chain" jump-target=bad_tcp protocol=tcp
add action=accept chain=prerouting comment="defconf: accept everything else from LAN" in-interface-list=LAN
add action=accept chain=prerouting comment="defconf: accept everything else from WAN" in-interface-list=WAN
add action=accept chain=prerouting comment="onuconf: accept everything else from ONU" in-interface-list=ONU
add action=drop chain=prerouting comment="defconf: drop the rest"
add action=drop chain=bad_tcp comment="defconf: TCP flag filter" protocol=tcp tcp-flags=!fin,!syn,!rst,!ack
add action=drop chain=bad_tcp comment="defconf: tcp-flags=fin,syn" protocol=tcp tcp-flags=fin,syn
add action=drop chain=bad_tcp comment="defconf: tcp-flags=fin,rst" protocol=tcp tcp-flags=fin,rst
add action=drop chain=bad_tcp comment="defconf: tcp-flags=fin,!ack" protocol=tcp tcp-flags=fin,!ack
add action=drop chain=bad_tcp comment="defconf: tcp-flags=fin,urg" protocol=tcp tcp-flags=fin,urg
add action=drop chain=bad_tcp comment="defconf: tcp-flags=syn,rst" protocol=tcp tcp-flags=syn,rst
add action=drop chain=bad_tcp comment="defconf: tcp-flags=rst,urg" protocol=tcp tcp-flags=rst,urg
add action=drop chain=bad_tcp comment="defconf: TCP port 0 drop" port=0 protocol=tcp log=yes log-prefix=fw_tcp_0_port
add action=accept chain=icmp4 comment="lanconf: accept echo reply from WAN" icmp-options=0:0 protocol=icmp in-interface-list=WAN
add action=accept chain=icmp4 comment="lanconf: accept net unreachable from WAN" icmp-options=3:0 protocol=icmp in-interface-list=WAN
add action=accept chain=icmp4 comment="lanconf: accept fragmentation needed from WAN" icmp-options=3:4 protocol=icmp in-interface-list=WAN
add action=accept chain=icmp4 comment="lanconf: accept time exceeded from WAN" icmp-options=11:0-255 protocol=icmp in-interface-list=WAN
add action=drop chain=icmp4 comment="lanconf: drop other ICMP from WAN" protocol=icmp in-interface-list=WAN
add action=accept chain=icmp4 comment="onuconf: accept echo reply from ONU" icmp-options=0:0 protocol=icmp in-interface-list=ONU
add action=drop chain=icmp4 comment="onuconf: drop other ICMP from ONU" protocol=icmp in-interface-list=ONU log=yes log-prefix=fw_drop_onu_icmp
add action=accept chain=icmp4 comment="defconf: echo reply" icmp-options=0:0 protocol=icmp in-interface-list=LAN log=yes log-prefix=fw_lan_ehco_reply
add action=accept chain=icmp4 comment="defconf: net unreachable" icmp-options=3:0 protocol=icmp in-interface-list=LAN
add action=accept chain=icmp4 comment="defconf: host unreachable" icmp-options=3:1 protocol=icmp in-interface-list=LAN
add action=accept chain=icmp4 comment="defconf: protocol unreachable" icmp-options=3:2 protocol=icmp in-interface-list=LAN
add action=accept chain=icmp4 comment="defconf: port unreachable" icmp-options=3:3 protocol=icmp in-interface-list=LAN
add action=accept chain=icmp4 comment="defconf: fragmentation needed" icmp-options=3:4 protocol=icmp in-interface-list=LAN
add action=accept chain=icmp4 comment="onuconf: echo to ONU" icmp-options=8:0 protocol=icmp in-interface-list=LAN dst-address-list=local_onu_ipv4
add action=accept chain=icmp4 comment="defconf: echo to local device" icmp-options=8:0 protocol=icmp in-interface-list=LAN dst-address-list=local_lan_ipv4
add action=drop chain=icmp4 comment="defconf: echo to non global" icmp-options=8:0 protocol=icmp in-interface-list=LAN dst-address-list=not_global_ipv4
add action=accept chain=icmp4 comment="defconf: echo to WAN" icmp-options=8:0 protocol=icmp in-interface-list=LAN
add action=accept chain=icmp4 comment="defconf: time exceeded" icmp-options=11:0-255 protocol=icmp in-interface-list=LAN
add action=drop chain=icmp4 comment="defconf: drop all other ICMP" protocol=icmp


# 设置 IPv4 黑洞路由
/ip route
add blackhole comment="defconf: RFC6890 for this host on this network" disabled=no dst-address=0.0.0.0/8
add blackhole comment="defconf: RFC6890 for private use" disabled=no dst-address=10.0.0.0/8
add blackhole comment="defconf: RFC6890 for shared address space" disabled=no dst-address=100.64.0.0/10
add blackhole comment="defconf: RFC6890 for loopback" disabled=no dst-address=127.0.0.0/8
add blackhole comment="defconf: RFC6890 for link local" disabled=no dst-address=169.254.0.0/16
add blackhole comment="defconf: RFC6890 for private use" disabled=no dst-address=172.16.0.0/12
add blackhole comment="defconf: RFC6890 for IETF protocol assignments" disabled=no dst-address=192.0.0.0/24
add blackhole comment="defconf: RFC6890 for DS-Lite" disabled=no dst-address=192.0.0.0/29
add blackhole comment="defconf: RFC6890 for TEST-NET-1" disabled=no dst-address=192.0.2.0/24
add blackhole comment="defconf: RFC6890 for 6to4 relay anycast" disabled=no dst-address=192.88.99.0/24
add blackhole comment="defconf: RFC6890 for private use" disabled=no dst-address=192.168.0.0/16
add blackhole comment="defconf: RFC6890 for benchmarking" disabled=no dst-address=198.18.0.0/15
add blackhole comment="defconf: RFC6890 for TEST-NET-2" disabled=no dst-address=198.51.100.0/24
add blackhole comment="defconf: RFC6890 for TEST-NET-3" disabled=no dst-address=203.0.113.0/24
add blackhole comment="defconf: RFC6890 for reserved" disabled=no dst-address=240.0.0.0/4
add blackhole comment="defconf: RFC6890 for limited broadcast" disabled=no dst-address=255.255.255.255/32
```

IPV6设置

```bash
##       Filter 规则 26 条
##          NAT 规则  5 条
##       Mangle 规则  1 条
##          Raw 规则 47 条
## Address-list 规则 19 条

/ipv6 firewall address-list
add address=fdac::2 comment="lanconf: local DNS server" list=local_dns_ipv6
add address=fdac::3 comment="lanconf: local DNS server" list=local_dns_ipv6
add address=fe80::/10 comment="defconf: RFC6890 Linked-Scoped Unicast" list=no_forward_ipv6
add address=ff00::/8 comment="defconf: multicast" list=no_forward_ipv6
add address=::1/128 comment="defconf: RFC6890 lo" list=bad_ipv6
add address=::ffff:0:0/96 comment="defconf: RFC6890 IPv4 mapped" list=bad_ipv6
add address=2001::/23 comment="defconf: RFC6890" list=bad_ipv6
add address=2001:db8::/32 comment="defconf: RFC6890 documentation" list=bad_ipv6
add address=2001:10::/28 comment="defconf: RFC6890 orchid" list=bad_ipv6
add address=::/96 comment="defconf: ipv4 compat" list=bad_ipv6
add address=100::/64 comment="defconf: RFC6890 Discard-only" list=not_global_ipv6
add address=2001::/32 comment="defconf: RFC6890 TEREDO" list=not_global_ipv6
add address=2001:2::/48 comment="defconf: RFC6890 Benchmark" list=not_global_ipv6
add address=fc00::/7 comment="defconf: RFC6890 Unique-Local" list=not_global_ipv6
add address=::/128 comment="defconf: unspecified" list=bad_dst_ipv6
add address=::/128 comment="defconf: unspecified" list=bad_src_ipv6
add address=ff00::/8 comment="defconf: multicast" list=bad_src_ipv6
add address=::/128 comment="ddosconf: DDoS" list=ddos_targets_ipv6
add address=::/128 comment="ddosconf: DDoS" list=ddos_attackers_ipv6


/ipv6 firewall filter
add action=accept chain=input comment="defconf: accept ICMPv6 after RAW" protocol=icmpv6
add action=accept chain=input comment="defconf: accept established,related,untracked" connection-state=established,related,untracked
add action=drop chain=input comment="defconf: drop invalid" connection-state=invalid
add action=accept chain=input comment="defconf: accept UDP traceroute" port=33434-33534 protocol=udp
add action=accept chain=input comment="defconf: accept DHCPv6-Client prefix delegation" dst-port=546 protocol=udp src-address=fe80::/10 log=yes log-prefix=fw_ipv6_pd
add action=accept chain=input comment="defconf: accept IKE" dst-port=500,4500 protocol=udp
add action=accept chain=input comment="defconf: accept IPSec AH" protocol=ipsec-ah
add action=accept chain=input comment="defconf: accept IPSec ESP" protocol=ipsec-esp
add action=drop chain=input comment="defconf: drop all not coming from LAN" in-interface-list=!LAN
add action=accept chain=forward comment="defconf: accept established,related,untracked" connection-state=established,related,untracked
add action=drop chain=forward comment="defconf: drop invalid" connection-state=invalid
add action=drop chain=forward comment="defconf: drop bad forward IPs" src-address-list=no_forward_ipv6
add action=drop chain=forward comment="defconf: drop bad forward IPs" dst-address-list=no_forward_ipv6
add action=drop chain=forward comment="defconf: rfc4890 drop hop-limit=1" hop-limit=equal:1 protocol=icmpv6
add action=accept chain=forward comment="defconf: accept ICMPv6 after RAW" protocol=icmpv6
add action=accept chain=forward comment="defconf: accept HIP" protocol=139
add action=accept chain=forward comment="defconf: accept IKE" dst-port=500,4500 protocol=udp
add action=accept chain=forward comment="defconf: accept AH" protocol=ipsec-ah
add action=accept chain=forward comment="defconf: accept ESP" protocol=ipsec-esp
add action=accept chain=forward comment="defconf: accept all that matches IPSec policy" ipsec-policy=in,ipsec
add action=drop chain=forward comment="defconf: drop everything else not coming from LAN" in-interface-list=!LAN
add action=jump chain=forward comment="ddosconf: DDoS" connection-state=new jump-target=detect_ddos
add action=return chain=detect_ddos comment="ddosconf: DDoS SYN-ACK Flood" dst-limit=32,32,src-and-dst-addresses/10s protocol=tcp tcp-flags=syn,ack log=yes log-prefix=fw_syn_ack_detected
add action=return chain=detect_ddos comment="ddosconf: DDoS" dst-limit=256,32,src-and-dst-addresses/10s
add action=add-dst-to-address-list chain=detect_ddos comment="ddosconf: DDoS" address-list=ddos_targets_ipv6 address-list-timeout=10m
add action=add-src-to-address-list chain=detect_ddos comment="ddosconf: DDoS" address-list=ddos_attackers_ipv6 address-list-timeout=10m log=yes log-prefix=fw_ddos_attackers


/ipv6 firewall nat
add action=masquerade chain=srcnat comment="defconf: masquerade IPv6" out-interface-list=WAN disabled=yes
add action=accept chain=dstnat comment="lanconf: accept local DNS server's query (UDP)" dst-port=53 in-interface-list=LAN protocol=udp src-address-list=local_dns_ipv6
add action=accept chain=dstnat comment="lanconf: accept local DNS server's query (TCP)" dst-port=53 in-interface-list=LAN protocol=tcp src-address-list=local_dns_ipv6 log=yes log-prefix=fw_dnsv6_tcp
add action=redirect chain=dstnat comment="lanconf: redirect DNS query (UDP)" dst-port=53 in-interface-list=LAN protocol=udp to-ports=53
add action=redirect chain=dstnat comment="lanconf: redirect DNS query (TCP)" dst-port=53 in-interface-list=LAN protocol=tcp to-ports=53 log=yes log-prefix=fw_dnsv6_tcp


/ipv6 firewall mangle
add action=change-mss chain=forward comment="defconf: fix IPv6 mss For WAN" new-mss=clamp-to-pmtu passthrough=yes protocol=tcp tcp-flags=syn


/ipv6 firewall raw
add action=accept chain=prerouting comment="defconf: enable for transparent firewall" disabled=yes
add action=drop chain=prerouting comment="ddosconf: DDoS" dst-address-list=ddos_targets_ipv6 src-address-list=ddos_attackers_ipv6
add action=accept chain=prerouting comment="defconf: RFC4291, section 2.7.1" dst-address=ff02:0:0:0:0:1:ff00::/104 icmp-options=135 protocol=icmpv6 src-address=::/128
add action=drop chain=prerouting comment="defconf: drop bogon IPs" src-address-list=bad_ipv6
add action=drop chain=prerouting comment="defconf: drop bogon IPs" dst-address-list=bad_ipv6
add action=drop chain=prerouting comment="defconf: drop packets with bad SRC ipv6" src-address-list=bad_src_ipv6
add action=drop chain=prerouting comment="defconf: drop packets with bad DST ipv6" dst-address-list=bad_dst_ipv6
add action=drop chain=prerouting comment="defconf: drop non global from WAN" in-interface-list=WAN src-address-list=not_global_ipv6
add action=drop chain=prerouting comment="defconf: drop bad UDP" port=0 protocol=udp log=yes log-prefix=fw_udp_0_port
add action=jump chain=prerouting comment="defconf: jump to ICMPv6 chain" jump-target=icmp6 protocol=icmpv6
add action=jump chain=prerouting comment="defconf: jump to TCP chain" jump-target=bad_tcp protocol=tcp
add action=accept chain=prerouting comment="defconf: accept local multicast scope" dst-address=ff02::/16
add action=drop chain=prerouting comment="defconf: drop other multicast destinations" dst-address=ff00::/8
add action=accept chain=prerouting comment="defconf: accept everything else from LAN" in-interface-list=LAN
add action=accept chain=prerouting comment="defconf: accept everything else from WAN" in-interface-list=WAN
add action=drop chain=prerouting comment="defconf: drop the rest"
add action=drop chain=bad_tcp comment="defconf: TCP flag filter" protocol=tcp tcp-flags=!fin,!syn,!rst,!ack
add action=drop chain=bad_tcp comment="defconf: tcp-flags=fin,syn" protocol=tcp tcp-flags=fin,syn
add action=drop chain=bad_tcp comment="defconf: tcp-flags=fin,rst" protocol=tcp tcp-flags=fin,rst
add action=drop chain=bad_tcp comment="defconf: tcp-flags=fin,!ack" protocol=tcp tcp-flags=fin,!ack
add action=drop chain=bad_tcp comment="defconf: tcp-flags=fin,urg" protocol=tcp tcp-flags=fin,urg
add action=drop chain=bad_tcp comment="defconf: tcp-flags=syn,rst" protocol=tcp tcp-flags=syn,rst
add action=drop chain=bad_tcp comment="defconf: tcp-flags=rst,urg" protocol=tcp tcp-flags=rst,urg
add action=drop chain=bad_tcp comment="defconf: TCP port 0 drop" port=0 protocol=tcp log=yes log-prefix=fw_tcp_0_port
add action=accept chain=icmp6 comment="defconf: rfc4890 drop ll if hop-limit!=255" dst-address=fe80::/10 hop-limit=not-equal:255 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: dst unreachable" icmp-options=1:0-255 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: packet too big" icmp-options=2:0-255 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: limit exceeded" icmp-options=3:0-1 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: bad header" icmp-options=4:0-2 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: echo request" icmp-options=128:0-255 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: echo reply" icmp-options=129:0-255 protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 multicast listener query only LAN" src-address=fe80::/10 icmp-options=130:0-255 in-interface-list=LAN protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 multicast listener query report only LAN" src-address=fe80::/10 icmp-options=131:0-255 in-interface-list=LAN protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 multicast listener query done only LAN" src-address=fe80::/10 icmp-options=132:0-255 in-interface-list=LAN protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 router solic only LAN" hop-limit=equal:255 icmp-options=133:0-255 in-interface-list=LAN protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 router advert only LAN" hop-limit=equal:255 icmp-options=134:0-255 in-interface-list=LAN protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 neighbor solic only LAN" hop-limit=equal:255 icmp-options=135:0-255 in-interface-list=LAN protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 neighbor advert only LAN" hop-limit=equal:255 icmp-options=136:0-255 in-interface-list=LAN protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 inverse ND solic only LAN" hop-limit=equal:255 icmp-options=141:0-255 in-interface-list=LAN protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 inverse ND advert only LAN" hop-limit=equal:255 icmp-options=142:0-255 in-interface-list=LAN protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 multicast listener report v2 only LAN" src-address=fe80::/10 icmp-options=143:0-255 in-interface-list=LAN protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 certificate path solicitation only LAN" hop-limit=equal:255 icmp-options=148:0-255 in-interface-list=LAN protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 certificate path advertisement only LAN" hop-limit=equal:255 icmp-options=149:0-255 in-interface-list=LAN protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 multicast router advertisement only LAN" src-address=fe80::/10 hop-limit=equal:1 icmp-options=151:0-255 in-interface-list=LAN protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 multicast router solicitation only LAN" src-address=fe80::/10 hop-limit=equal:1 icmp-options=152:0-255 in-interface-list=LAN protocol=icmpv6
add action=accept chain=icmp6 comment="defconf: rfc4890 multicast router termination only LAN" src-address=fe80::/10 hop-limit=equal:1 icmp-options=153:0-255 in-interface-list=LAN protocol=icmpv6
add action=drop chain=icmp6 comment="defconf: drop all other ICMP" protocol=icmpv6


/ipv6 route
add blackhole comment="defconf: RFC6890 for loopback address" disabled=no dst-address=::1/128
add blackhole comment="defconf: RFC6890 for unspecified address" disabled=no dst-address=::/128
add blackhole comment="defconf: RFC6890 for IPv4-IPv6 translat" disabled=no dst-address=64:ff9b::/96
add blackhole comment="defconf: RFC6890 for IPv4-mapped address" disabled=no dst-address=::ffff:0:0/96
add blackhole comment="defconf: RFC6890 for discard-only address block" disabled=no dst-address=100::/64
add blackhole comment="defconf: RFC6890 for IETF protocol assignments" disabled=no dst-address=2001::/23
add blackhole comment="defconf: RFC6890 for TEREDO" disabled=no dst-address=2001::/32
add blackhole comment="defconf: RFC6890 for benchmarking" disabled=no dst-address=2001:2::/48
add blackhole comment="defconf: RFC6890 for documentation" disabled=no dst-address=2001:db8::/32
add blackhole comment="defconf: RFC6890 for ORCHID" disabled=no dst-address=2001:10::/28
add blackhole comment="defconf: RFC6890 for 6to4" disabled=no dst-address=2002::/16
add blackhole comment="defconf: RFC6890 for unique-local" disabled=no dst-address=fc00::/7
add blackhole comment="defconf: RFC6890 for linked-scoped unicast" disabled=no dst-address=fe80::/10
```





开启UPnP设置

1、点击“IP” -- “UPNP”，将Enabled（启用）和Allow To Disable External Interface（允许禁用外部接口），打钩并点击Apple，OK，保存设置。

```
# IP / UPnP 
Enabled: yes
Allow To Disable External Interface: yes
Show Dummy Rule: yes
```

2、重新打开“IP” -- “UPNP”，UPNP Settings界面，点击Interfaces，然后在UPnP Interface Settings界面点击“+”号，添加2条配置。

```
- 外网 - Interface：pppoe-out1(如果是PPPOE接入外网，就填pppoe-out1接口名，静态IP接入就填WAN接口名)，type：external。
- 内网 - Interface：bridge1（网桥名称，如未使用网桥则选择LAN口），type：internal。  
```





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

