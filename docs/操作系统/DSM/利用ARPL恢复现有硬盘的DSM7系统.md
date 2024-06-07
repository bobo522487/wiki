# 利用ARPL恢复现有硬盘的DSM7系统

 2023年2月6日 35条评论 9.32k次阅读 7人点赞 博主

很多群晖NAS玩家应该会遇到过以下场景：

★之前用物理机安装群晖系统，现在改成了虚拟机安装；

★之前用虚拟机安装群晖系统，现在改成了物理机安装；

★之前用虚拟机的操作系统，现在要换成了别的操作系统（比如：PVE换成ESXI、ESXI换到PVE、PVE换成UNRAID，诸如此类）

★U盘引导盘坏了，需要重新做一个；

★之前用U盘做引导盘，现在想换成SSD引导；

★之前用SSD做引导盘，现在想换成U盘引导；

等等......

如果你的硬盘是DSM7系统，那么可以利用ARPL来快速的恢复硬盘的DSM7系统。

 

------

操作步骤：

1、把带有DSM7系统的硬盘装到做NAS的电脑主机上，在另外的电脑下载ARPL最新版本的IMG，做成引导盘启动（如果你还不知道怎样做，那么建议先去学习一下《[史上最简单的黑群晖DSM7.X引导编译方法，小学生都能操作！](https://wp.gxnas.com/12245.html)》这篇教程），启动完成后屏幕上会显示一个IP地址，记下来；

[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661218-1.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661218-1.jpg)

 

 

2、在电脑浏览器打开这个地址；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661219-2.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661219-2.jpg)

 

 

3、按向下的方向键，移动到“Advanced menu”处，回车；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661219-3.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661219-3.jpg)

 

 

4、按向下的方向键，移动到“Try to recovery a DSM installed system”处，回车；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661220-4.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661220-4.jpg)

 

 

5、我这个硬盘装的是DS923+的系统，版本是7.11-42962，系统已经识别出来了，按回车；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661221-5.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661221-5.jpg)

 

 

6、此时看到网页左上角把从硬盘读取到的信息自动选择好了；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661221-6.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661221-6.jpg)

 

 

7、按向下的方向键，移动到“Exit”处，回车；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661223-7.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661223-7.jpg)

 

 

8、按向下的方向键，移动到“Build the loader”处，回车；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661224-8.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661224-8.jpg)

 

 

9、这个处理过程很快；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661224-9.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661224-9.jpg)

 

 

10、处理完成后，系统自动跳回菜单，移动方向键到“Advanced menu”处，回车；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661225-10.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661225-10.jpg)

 

 

11、移动方向键到“Switch direct boot：false”处，回车；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661226-11.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661226-11.jpg)

 

 

12、使“Switch direct boot：false”变成“Switch direct boot：true”，就好了；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661227-12.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661227-12.jpg)

 

 

13、按向下的方向键，移动到“Exit”处，回车；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661227-13.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661227-13.jpg)

 

 

14、按向下的方向键，移动到“Boot the loader”处，回车；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661228-14.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661228-14.jpg)

 

 

15、当NAS物理主机屏幕（或者是NAS虚拟机的屏幕）显示“Reboot to boot directly in DSM”的时候，表示系统即将重启，请耐心等待启动完成；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661228-15.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661228-15.jpg)

 

 

16、当重启完成后，会显示如下界面就不动了，不要以为是机器死机或者卡住了；[![img](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661229-16.jpg)](https://wp.gxnas.com/wp-content/uploads/2023/02/1675661229-16.jpg)

 

 

17、耐心等待几分钟，具体等待的时间由硬件性能决定，正常情况3-5分钟以内，在同一个局域网内的另外一台电脑用群晖助手（Synology Assistant）或者在浏览器打开【[这个地址](https://finds.synology.com/)】来搜索群晖的IP地址，或者直接进路由器找IP也可以；

 

 

18、在电脑浏览器打开群晖的IP地址，就可以登录系统咯。