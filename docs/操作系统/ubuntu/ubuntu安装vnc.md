

```
sudo apt-get update
sudo apt-get install lightdm -y	# 显示管理器更改为 lightdm
sudo reboot

```



```
sudo apt-get install x11vnc


sudo nano /lib/systemd/system/x11vnc.service
```

and copy paste in the following

```
[Unit]
Description=x11vnc service
After=display-manager.service network.target syslog.target

[Service]
Type=simple
ExecStart=/usr/bin/x11vnc -forever -display :0 -auth guess -passwd 522487
ExecStop=/usr/bin/killall x11vnc
Restart=on-failure

[Install]
WantedBy=multi-user.target
```



```
systemctl daemon-reload
systemctl enable x11vnc.service
systemctl start x11vnc.service

systemctl status x11vnc.service
```


设置->privacy->ScreenLock，关闭三项选择；

![img](https://www.crazy-logic.co.uk/wp-content/uploads/2020/04/image.png)

```
roboot
```



So this isn’t so secure so you might need to install something called xscreensaver.
