### 安装HAProxy

利用HAProxy实现kubeapi服务的负载均衡

```shell
# 修改内核参数
cat >> /etc/sysctl.conf <<EOF
net.ipv4.ip_nonlocal_bind = 1
EOF

# 从指定的文件加载系统参数，如不指定即从/etc/sysctl.conf中加载
sysctl -p

# 安装配置HAProxy
apt update
apt -y install haproxy

# 修改配置
cat >> /etc/haproxy/haproxy.cfg <<EOF
listen stats
	mode http
	bind *:1080
	stats enable
	log global
	stats uri /status
	stats auth admin:123456
listen kubernetes-api-6443
	bind 0.0.0.0:6443
	mode tcp
	server k8s-master1.t-plus.com.cn 10.10.10.31:6443 check inter 3s fall 3 rise 3
	server k8s-master2.t-plus.com.cn 10.10.10.32:6443 check inter 3s fall 3 rise 3
	server k8s-master3.t-plus.com.cn 10.10.10.33:6443 check inter 3s fall 3 rise 3
EOF

# 重启服务
systemctl restart haproxy
```

### 安装Keepalived

安装keepalived实现HAProxy高可用

```shell
# 安装keepalived
apt update
apt -y install keepalived

# 编辑keepalived的配置文件
vim /etc/keepalived/keepalived.conf

! Configuration File for keepalived
global_defs {                   #全局参数
  router_id k8s-ha1.t-plus.com.cn   #指定名称，各个服务器名称要不一样
}

vrrp_script check_haproxy {
  script "/etc/keepalived/check_haproxy.sh"
  interval 3
  weight -30
  fall 3
  rise 2
  timeout 2
}

vrrp_instance VI_1 {            #指定vrrp热备参数
  state MASTER                  #服务器角色是master，备份服务器设置为BACKUP
  interface ens160               #修改物理网卡名称 
  virtual_router_id 10          #组号相同
  priority 100                  #优先级，主服务器设置要大于备服务器
  advert_int 1
  authentication {
   auth_type PASS               #验证类型和密码，不建议修改
   auth_pass 123456
}
virtual_ipaddress {
  10.10.10.30/24               #漂移地址（VIP）地址，可以有多个
 }
track_script{
  check_haproxy
}


# 编写脚本
cat > /etc/keepalived/check_haproxy.sh <<EOF
#!/bin/bash
/usr/bin/killall -O haproxy || systemctl restart haproxy
EOF

chmod a+x /etc/keepalived/check_haproxy.sh
systemctl restart keepalived

```

```shell
#!/bin/bash
 
STAT=`ps -C haproxy --no-header | wc -l`
 
if [[ ! "$STAT" -eq 1  ]];then
        /etc/init.d/keepalived stop
fi
```

