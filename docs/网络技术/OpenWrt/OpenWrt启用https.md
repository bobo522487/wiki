### OpenWrt启用https



检查是否安装uhttpd软件包

```
# vi /etc/config/uhttpd
```



上传并修改证书文件

        option cert '/etc/uhttpd.cer'
        option key '/etc/uhttpd.key'



重启uhttpd服务

```
/etc/init.d/uhttpd restart
```

