

## PVE安装群晖-核显转码



### 上传arpl镜像，复制并记录文件路径。

```shell
/var/lib/vz/template/iso/arpl.img
```



### 创建虚拟机

```
常规
  名称：SA6400
操作系统
  光驱：不使用任何介质
系统
  显卡：无		机型：q35		BIOS：WVMF(UEFI)
磁盘
  总线/设备：SATA
  磁盘大小(GiB): 100 #建议大小
CPU
  核心：4		类别：host
内存
  内存(MiB): 8192
网络： 无网络设备
```

### **编辑虚拟机**

硬件/BIOS/改为UEFI

添加硬盘直通设备，默认配置如下：SATA controller: JMicron Technology Corp. JMB58x AHCI SATA controller~

```添加
设备：0000:01:00.0
所有功能： 是 	 主GPU：否
ROM-Bar: 是		PCI-Express: 是
```

添加核显直通设备，默认配置如下：

```添加
设备：0000:00:02.0
所有功能： true 	 主GPU：true
ROM-Bar: false	PCI-Express: true
```

添加网卡直通设备，默认配置如下：

```添加
设备：0000:02:00.0		参数默认
```

添加NVME直通设备，默认配置如下：

```
设备：0000:05:00.0		参数默认
设备：0000:06:00.0		参数默认
```

添加串行端口:

```
串行端口: 0
```

删除无用设备，如光驱/虚拟网卡

配置选项

```
开启自启动：是
引导顺序：sata0
```



添加RDM直通

```
qm set 100 -sata1 /dev/disk/by-id/XXX
qm set 100 -sata2 /dev/disk/by-id/XXX
```



### 输入命令

选择宿主机/Shell，输入以下命令（注意虚拟机ID）

```
nano /etc/pve/qemu-server/101.conf
```

```shell
# 在首行添加以下代码
args: -device 'nec-usb-xhci,id=usb-bus0,multifunction=on' -drive 'file=/var/lib/vz/template/iso/arpl.img,media=disk,format=raw,if=none,id=drive-disk-bootloader' -device 'usb-storage,bus=usb-bus0.0,port=1,drive=drive-disk-bootloader,id=usb-disk-bootloader,bootindex=999,removable=on'
```



### 安装群晖

启动虚拟机，打开控制台/xterm.js.

启动完成，输入root免密登录。输入ip a查看ip地址。

打开浏览器，输入 IP:7681进入设置菜单。

选择：构建引导， 启动引导。

重启完成后，直接访问IP。

上传pat文件，等待重启。



### 配置群晖

创建存储池

控制面板/共享文件夹 /创建/名称：share

```
文件管理/属性/权限/新增：  用户或组：Everyone	读取和写入权限；应用到这个文件夹/子文件夹及文件。
```

控制面板/文件服务：启用NFS服务，协议NFSv4.1

安装docker套件

开启并登录ssh，验证硬解

```bash
ls -l /dev/dri
```

```
card0
renderD128
```





# 附录

## 1. 镜像下载地址

链接: https://pan.baidu.com/s/1Qz6nrsJWFXzO75LQso7ItA?pwd=3333 提取码: 3333

国外分流：https://ttttt.link/f/64182de86e818

## 2. 系统下载地址

https://cndl.synology.cn/download/DSM/release/7.1.1/42962-4/DSM_SA6400_42962.pat