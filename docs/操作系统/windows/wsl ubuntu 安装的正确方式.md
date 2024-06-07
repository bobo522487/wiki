# wsl ubuntu 安装的正确方式





控制面板 -> 程序 -> 卸载程序，添加下述2项：

![](https://img-blog.csdnimg.cn/direct/e1bf247bc5944da6a353e7242b65ae5a.png)



##### 打开powershell

```

wsl --set-default-version 2		# 设置wsl的版本为2
wsl --update					# 更新wsl程序
wsl --shutdown					# 强制关闭子系统

wsl --list --online				# 查看wsl支持的列表
wsl --list --verbose	# 列出已安装的 Linux 发行版
wsl --install -d Ubuntu-24.04	# 安装指定版本的系统
wsl --unregister Ubuntu-24.04	# 删除WSL的Ubuntu发行版

wsl --shutdown
wsl --export Ubuntu-18.04 D:\WSL2\Ubuntu-18.04.2.0.tar
```



```
!安装GUI命令:
sudo apt update && sudo apt -y upgrade
sudo apt-get purge xrdp
sudo apt install -y xrdp
sudo apt install -y xfce4
sudo apt install -y xfce4-goodies

sudo cp /etc/xrdp/xrdp.ini /etc/xrdp/xrdp.ini.bak
sudo sed -i 's/3389/3389/g' /etc/xrdp/xrdp.ini
sudo sed -i 's/max_bpp=32/#max_bpp=32\nmax_bpp=128/g' /etc/xrdp/xrdp.ini
sudo sed -i 's/xserverbpp=24/#xserverbpp=24\nxserverbpp=128/g' /etc/xrdp/xrdp.ini
echo xfce4-session > ~/.xsession

sudo nano /etc/xrdp/startwm.sh
!以下这两行注释掉:
#test -x /etc/X11/Xsession && exec /etc/X11/Xsession
#exec /bin/sh /etc/X11/Xsession

!添加这一行:
# xfce
startxfce4

sudo /etc/init.d/xrdp start

!WINDOWS远程连接
localhost:3389
```



安装vcxsrv windows x server，google搜索vcxsrv

```
Display number -1 改为 0
Native opengl  取消对勾
Disable access control  打上对勾
```

在ubuntu终端运行命令

```
export GAZEBO_IP=127.0.0.1
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0 
export LIBGL_ALWAYS_INDIRECT=0
```

运行 gz sim出现gui，再次运行rviz2时，需再次运行`export LIBGL_ALWAYS_INDIRECT=0`命令
