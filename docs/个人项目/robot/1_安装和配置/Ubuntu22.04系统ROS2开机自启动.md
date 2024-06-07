# Ubuntu22.04系统ROS2开机自启动



```

source /opt/ros/humble/setup.bash
source /root/ros2_ws/install/setup.bash
```





```
[Unit]
Description=ros2 launch script
 
[Service]
Type=simple
 
# 指定用户名，也就是Ubuntu系统下当前的用户名
User=$your_name$    
 
# 运行脚本xxx.sh，确保脚本具备可执行权限,具体指令写在xxx.sh中
ExecStart=/root/ros_ws/rc.sh
 
PrivateTmp=true
KillMode=control-group
 
[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload    # 重新加载服务
systemctl start rc.service      # 启动服务
systemctl status rc.service     # 查看服务状态
systemctl enable rc.service     # 开机启动

```

深度相机

```

#安装udev
sudo apt install udev -y

```



