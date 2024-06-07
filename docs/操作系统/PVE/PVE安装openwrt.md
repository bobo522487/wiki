### PVE安装openwrt



上传img镜像文件，保持上传地址

```
/var/lib/vz/template/iso/istoreos-21.02.3-2023040712-x86-64-squashfs-combined-efi.img
```



**3. 导入镜像**

选择宿主机，进入命令行

```
qm importdisk 100 /var/lib/vz/template/iso/istoreos-21.02.3-2023040712-x86-64-squashfs-combined-efi.img local-lvm
```

注意 VM ID 100 (100是 虚拟机 ID) 和路径 以及镜像名称 , 最后又 local-lvm