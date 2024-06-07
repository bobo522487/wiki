

## Ubuntu22.04配置rsync服务



```
# 安装
sudo apt-get install rsync

sudo sed -i 's/RSYNC_ENABLE=false/RSYNC_ENABLE=true/' /etc/default/rsync

echo "max connections = 2
log file = /var/log/rsync.log
timeout = 300
Charset = UTF-8

[plot] # 模块名
comment = Public Share
# path为需要同步的文件夹路径
path = /mnt/plottemp
read only = no
list = yes
uid = root
gid = root
# 必须和 rsyncd.secrets中的用户名对应
auth users = chia
secrets file = /etc/rsyncd.secrets
"  > /etc/rsyncd.conf

# 设置用户和密码
echo "chia:r5yncd"  > /etc/rsyncd.secrets

sudo chmod 600 /etc/rsyncd.secrets
sudo /etc/init.d/rsync restart
```

