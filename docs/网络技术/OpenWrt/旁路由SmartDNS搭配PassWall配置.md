# 旁路由SmartDNS搭配PassWall配置



配置openwrt

```

# DHCP/DNS - HOST和解析文件
使用/etc/ethers配置 勾选
忽略/etc/hosts 勾选
```



vim /etc/config/smartdns

```
config smartdns
	option enabled '1'
	option server_name 'smartdns'
	option port '6053'
	option tcp_server '1'
	option ipv6_server '1'
	option dualstack_ip_selection '1'
	option prefetch_domain '1'
	option serve_expired '1'
	option redirect 'none'
	option cache_size '32768'
	option rr_ttl '600'
	option rr_ttl_min '300'
	option rr_ttl_max '600'
	option coredump '0'
	option seconddns_enabled '1'
	option seconddns_port '6553'
	option seconddns_tcp_server '1'
	option seconddns_server_group 'foreign'
	option seconddns_no_speed_check '1'
	option seconddns_no_rule_addr '1'
	option seconddns_no_rule_nameserver '1'
	option seconddns_no_rule_ipset '0'
	option seconddns_no_rule_soa '1'
	option seconddns_no_dualstack_selection '1'
	option seconddns_no_cache '1'
	option force_aaaa_soa '0'
	list old_redirect 'none'
	list old_port '6053'
	list old_enabled '0'

config server
        option enabled '1'
		option name 'gzdx1_udp'
		option ip '202.98.198.167'
        option blacklist_ip '0'
        option type 'udp'
        option server_group 'cn'

config server
        option enabled '1'
		option name 'gzdx2_udp'
		option ip '202.98.192.67'
        option blacklist_ip '0'
        option type 'udp'
        option server_group 'cn'

config server
        option enabled '1'
		option name 'ali_udp'
		option ip '223.5.5.5'
        option blacklist_ip '0'
        option type 'udp'
        option server_group 'cn'

config server
        option enabled '1'
		option name 'tencent_udp'
		option ip '119.29.29.29'
        option blacklist_ip '0'
        option type 'udp'
        option server_group 'cn'

config server
        option enabled '1'
        option type 'udp'
        option name 'baidu-ipv6'
        option ip '2400:da00::6666'

config server
        option enabled '1'
        option type 'udp'
        option name 'aliyun-ipv6'
        option ip '2400:3200::1'

config server
	option enabled '1'
	option blacklist_ip '0'
	option name 'google'
	option ip '8.8.8.8'
	option type 'tcp'
	option server_group 'foreign'
	option addition_arg '-exclude-default-group'

config server
	option enabled '1'
	option name 'cloudflare'
	option ip '1.1.1.1'
	option type 'tcp'
	option server_group 'foreign'
	option blacklist_ip '0'
	option addition_arg '-exclude-default-group'

config server
	option enabled '1'
	option name 'QUAD9'
	option ip '9.9.9.9'
	option type 'tcp'
	option blacklist_ip '0'
	option server_group 'foreign'
	option addition_arg '-exclude-default-group'


```

passwall设置

DNS分流选择SmartDNS

国内分组名 cn

过滤模式 通过UDP请求DNS

远程DNS 127.0.0.1:6553