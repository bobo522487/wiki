# 在 PVE 7 中启用硬件直通功能

## 一：RDM磁盘直通

RDM磁盘直通，不需要开启iommu。只能在PVE命令行中添加。

我们可以通过下面命令，列出当前的硬盘列表

```bash
ls -la /dev/disk/by-id/|grep -v dm|grep -v lvm|grep -v part
```

nvme开头的是nvme硬盘，ata开头是走sata或者ata通道的设备。，scsi是scsi设备-阵列卡raid或者是直通卡上的硬盘。

我们可以通过`qm set <vmid> --scsiX /dev/disk/by-id/xxxxxxx` 进行RDM直通

例如你有一个虚拟机，虚拟机的vmid是101，--scsiX，这里的X是整数，最多为如果你不清楚vmid这个是什么含义，你可以参考下面文章

[认识虚拟机VMID的作用](https://foxi.buduanwang.vip/virtualization/pve/1643.html/)

当然，你也可以使用ide或者sata形式直通硬盘，如下

```bash
qm set 101 --sata1 /dev/disk/by-id/ata-WUH721818ALE6L4_3FG4RRST 
qm set 101 --sata2 /dev/disk/by-id/ata-WDC_WUH721818ALE6L4_3RHDMVMA 
```

**启用IOMMU功能**

用网页端的 PVE shell 或 ssh 连接至 PVE，输入以下命令：

```bash
nano /etc/default/grub
```

在文档中找到 “GRUB_CMDLINE_LINUX_DEFAULT=”quiet””一行，

**对于 Intel CPU 用户**，将改行修改为：

```json
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on iommu=pt"
```

修改完成后，按 Ctrl+O 保存，按 Ctrl+X 退出文本编辑器。

然后输入下一行命令更新 Grub：

```bash
update-grub
```

**加载相应的内核模块**

在命令行中输入以下命令：

```json
echo vfio >> /etc/modules
echo vfio_iommu_type1 >> /etc/modules
echo vfio_pci >> /etc/modules
echo vfio_virqfd >> /etc/modules
```

然后输入

```bash
update-initramfs -k all -u
```

来更新内核参数。然后**重启 PVE**。

**验证IOMMU是否开启成功**

重启之后，在命令行输入以下命令：

```bash
dmesg | grep iommu
```

若有如类似于下图回显，则说明开启成功：

![img](https://never-blog.oss-cn-beijing.aliyuncs.com/wp-content/uploads/2022/08/20220822174019817.png!full)

再输入：

```bash
find /sys/kernel/iommu_groups/ -type l
```

如果有类似于下图回显，就代表成功：

![img](https://never-blog.oss-cn-beijing.aliyuncs.com/wp-content/uploads/2022/08/20220822174138373.png!full)



