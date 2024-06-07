



```
# 修改主机名
sudo hostnamectl set-hostname plot01

# 修改时区
timedatectl set-timezone Asia/Shanghai

# 修改固定IP地址
cp /etc/netplan/00-installer-config.yaml /etc/netplan/00-installer-config.yaml.bak
echo "# This is the network config written by 'subiquity'
network:
  ethernets:
    ens33:
      dhcp4: no
      addresses: [10.10.10.29/24]
      nameservers:
          addresses: [114.114.114.114,8.8.8.8]
      routes:
        - to: default
          via: 10.10.10.2
  version: 2" > /etc/netplan/00-installer-config.yaml
netplan apply

# ubuntu 安装VMware tools
sudo apt install open-vm-tools-desktop

# ubuntu 22.04 更换源
/etc/apt/sources.list /etc/apt/sources.list.bak	#22.04 
/etc/apt/sources.list.d/ubuntu.sources			#24.04
用下面内容替换
http://mirrors.aliyun.com/ubuntu/

sudo apt update
sudo apt upgrade -y

```



```

# 已经初始化分区后的Ubuntu系统，快速扩容
sudo lvextend -l +100%FREE /dev/mapper/ubuntu--vg-ubuntu--lv
sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv

# 硬盘克隆
dd if=/dev/sda of=/dev/sdb bs=4096 progress=yes

# 查看硬盘uuid
lsblk -o name,uuid,size | awk -v drive="sda" '$1 == drive {print $2}'
# 查看硬盘序列号
smartctl -a "/dev/sda" | grep "Serial Number" | awk '{print $3}'


echo "$(blkid /dev/nvme0n1 | awk '{print $2}') /mnt/plottemp defaults 0 0" >> /etc/fstab

```

