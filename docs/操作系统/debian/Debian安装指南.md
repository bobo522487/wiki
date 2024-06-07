### 更改语言环境

输出乱码，需修改配置文件

```
vi .bashrc

# 最下面增加
export LANG=C
```

保存退出即可。如需立即生效，输入以下命令

```
source .bashrc
```



### 配置网络

一、对于有线网络，如果默认没有安装图形界面，进入了 multi-user.target中时，是没有使用NetworkManager管理网络的，此时需要手动配置才能上网
首先得到网卡名称：ip addr or ls /sys/class/net/，以下假设网卡名为eth0，实际中应替换为自己实际的名称。

设置文件为：/etc/network/interfaces
使用DHCP方式，在文件底部添加：

```
auto eth0
allow-hotplug eth0
iface eth0 inet dhcp
```


手动设置IP上网，在文件底部添加：

```
auto eth0
iface eth0 inet static
    address 192.168.0.7
    netmask 255.255.255.0
    gateway 192.168.0.254
```

重启网络服务sudo systemctl restart networking.service
详细的设置方法可以使用man interfaces得到
也可以参考这里：https://wiki.debian.org/NetworkConfiguration



### Debian11更换阿里源

备份源文件

cp /etc/apt/sources.list /etc/apt/sources.list_backup
编辑源文件

```
vi /etc/apt/sources.list 

#添加如下
deb http://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ bullseye main non-free contrib
deb http://mirrors.aliyun.com/debian-security/ bullseye-security main
deb-src http://mirrors.aliyun.com/debian-security/ bullseye-security main
deb http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib
deb http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib
```

#然后

```
apt-get update
```



### 升级内核

下载内核

```
mkdir kernel
cd kernel
wget http://ftp.debian.org/debian/pool/main/l/linux-signed-amd64/linux-image-6.1.0-7-amd64_6.1.20-2_amd64.deb
```

升级内核

```
dpkg -i *.deb
```



```
apt install curl -y

mkdir -p /lib/firmware/i915 && cd /lib/firmware/i915
curl -LO https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/i915/ehl_guc_70.1.1.bin
curl -LO https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/i915/ehl_huc_9.0.0.bin
curl -LO https://git.kernel.org/pub/scm/linux/kernel/git/firmware/linux-firmware.git/plain/i915/icl_dmc_ver1_09.bin

#备用下载地址：https://anduin.linuxfromscratch.org/sources/linux-firmware/i915/
```

开启核显低功耗编码

```
nano /etc/modprobe.d/i915.conf
-----------------------------
options i915 enable_guc=3
```

严重开启成功

```
journalctl -b -o short-monotonic -k | egrep -i "i915|dmr|dmc|guc|huc"

```

挂载nfs

```
10.10.10.28:/volume1/share/media /mnt/nas_nfs nfs x-systemd.automount,x-systemd.after=network-online.target 0 0
```



一键安装docker

```
curl -sSL https://get.daocloud.io/docker | sh

#接着设定docker服务
systemctl start docker
systemctl enable docker
```

