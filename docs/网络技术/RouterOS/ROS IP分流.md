ROS IP分流



```
# 导入中国IP地址列表
/tool fetch url=http://www.iwik.org/ipcountry/mikrotik/CN
/import file-name=CN

# 新建Routing/Tables

```

新建Routing/Tables，

```
# Routing / Tables
name: openwrt
FIB: 是
```

新建允许出国地址列表 

```
#  IP / Firewall / Address Lists / 新建
Name: proxy
Address: 10.10.10.1-10.10.10.254
```

**设置Mangle**

放行本地网段所有流量

```
#  IP / Firewall / Mangle / 新建
General
    Chain: prerouting
    Src. Address: 10.10.10.0/24
Action
	Action: mark accept
```

出国流量打路由标记openwrt

```
#  IP / Firewall / Mangle / 新建
General
    Chain: prerouting
    Src. Address: Proxy
    Dst. Address: ! CN	
Action
	Action: mark routing
	New Routing Mark: openwrt
```

**设置IP Tables**

路由标记为openwrt的流量走旁路由

```
# IP / Tables / 新建
st. Address: 0.0.0.0/0
Gateway: 10.10.10.2 # openwrt的IP地址
Dsitance: 1
Scope: 30
Target Scope: 10
Routing Table: openwrt
```



**设置自动任务**

```
/file remove CN
/tool fetch url=http://www.iwik.org/ipcountry/mikrotik/CN
/import file-name=CN
```

**监控旁路有上下线**

```
$ Tools / Netwatch / 新建
Host
	Host: 10.10.10.2
	Interval: 00:05:00 # 5分钟监测一次
	Timeout: 1
Up
	/ip firewall mangle enable number=2		#number需对应Firewall/Mangle序号
Down
	/ip firewall mangle disable number=2 	#number需对应Firewall/Mangle序号
```





