# 关于黑群晖使用11代CPU开启核显硬解那些事（使用ARPL开启编译SA6400引导的教程）

 2023年2月23日 48条评论 13.59k次阅读 7人点赞 博主

​    大多玩黑群的人都知道，目前由于群晖内核版本低的原因，无法使用11代或11代以上CPU开启核显硬解，直到上周在B站有UP主发布了11代CPU开启群晖硬解的视频，于是有很多小伙伴就联系博主：能不能做个引导、能不能写个教程之类，那博主今天就来聊聊一下黑群晖使用11代CPU开启核显硬解那些事以及顺便写个教程吧。

​    黑群晖使用11代CPU开启核显硬解的原理：由于之前我们使用到的DS3615/DS3617/DS918/DS920/DVA3221/DS1622/DS920等黑群系统，这些系统内核版本最高才是4.4，而Intel11代的CPU要求Linux内核版本必须在5.10以上才可以驱动核显开启硬解，于是大佬们又“创造”了一个新的黑群系统SA6400，内核版本是5.10，刚好可以驱动11代的GPU开启硬解。但是目前SA6400还在完善的阶段，还有许多不足之处（比如：需要使用PVE虚拟机模拟U盘启动、不支持SATA启动、网卡驱动支持不多等等），所以不能大范围的安装和使用，目前仅供动手强力较的人先玩玩。

​    成品的SA6400引导文件我就不放出来下载了，如果感兴趣的话可以继续看下面编译SA6400引导的教程：

1、去【[ARPL的仓库](https://github.com/fbelavenuto/arpl)】下载ARPL最新版本（截止2023年2月23日，ARPL的最新版本为v1.1-bate2），如果不会，建议先学习《[黑群晖DSM7.X引导用arpl编译教程](https://wp.gxnas.com/12245.html)》；

 

2、使用U盘刷入ARPL引导文件，在PVE建立虚拟机使用模拟U盘启动，使用模拟U盘启动需要设置：机型设置为 q35、启动方式使用UEFI方式，编辑`/etc/pve/qemu-server/SA6400虚拟机的id.conf` ，在文件添加下面内容（注意：需要自行替换arpl.img文件的路径）:

```
args: -device 'nec-usb-xhci,id=usb-bus0,multifunction=on' -drive 'file=/var/lib/vz/template/iso/arpl.img,media=disk,format=raw,if=none,id=drive-disk-bootloader' -device 'usb-storage,bus=usb-bus0.0,port=1,drive=drive-disk-bootloader,id=usb-disk-bootloader,bootindex=999,removable=on'
```

3、启动后记录一下IP地址以及root的密码，如下图两处：

[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118935-2.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118935-2.jpg)

 

 

4、在电脑上打开SSH工具，我使用的是MobaXterm，填写上一步骤获取到的IP地址，用户名为root，端口22，登录；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118937-3.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118937-3.jpg)

 

 

5、输入密码Redp1lL-1s-4weSomE登录到如下界面；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118938-4.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118938-4.jpg)

 

 

6、由于SA6400还在测试阶段，默认ARPL不显示该型号，所以需要魔改一下，复制以下代码到SSH的窗口下粘贴，敲回车运行（将来SA6400系统开发成熟以后，ARPL能直接有显示SA6400的话，此步骤就不需要做了）；

```
curl -skL https://raw.githubusercontent.com/wjz304/Redpill_CustomBuild/main/arpl-sa6400.sh | bash
```

 

[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118939-5.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118939-5.jpg)

 

 

7、显示有“Opening... SA6400 is exist!”字样的时候就表示Ok了，如果长时间卡住没有输出信息的话请重新打开SSH工具重新做一次；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118940-6.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118940-6.jpg)

 

 

9、在电脑浏览器打开第3步获取到的IP地址，后面加:7681，回车，进入ARPL编译菜单，在第一行“Choose a model”处回车；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118941-7.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118941-7.jpg)

 

 

10、在“Show bate models”处回车；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118942-8.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118942-8.jpg)

 

 

11、此时编译系统就能看到有SA6400这个型号出来了；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118944-9.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1677118944-9.jpg)

 

 

12、参考《[黑群晖DSM7.X引导用arpl编译教程](https://wp.gxnas.com/12245.html)》后续的教程，继续操作。