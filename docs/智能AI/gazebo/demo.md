# Ubuntu 上的二进制安装[![img](https://gazebosim.org/assets/icon/baseline-link-24px.svg)](https://gazebosim.org/docs/fortress/install_ubuntu#binary-installation-on-ubuntu)



*****需要关闭虚拟机3d加速*****

Fortress 二进制文件适用于 Ubuntu Bionic、Focal 和 Jammy。所有 Fortress 二进制文件都托管在 osrfoundation 存储库中。要安装所有这些，`ignition-fortress`可以安装元包。

首先安装一些必要的工具：

```
sudo apt-get update sudo apt-get install lsb-release wget gnupg
```

然后安装Ignition Fortress:

```
sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null sudo apt-get update sudo apt-get install ignition-fortress
```

所有库都应该准备好使用，并且`ign gazebo`应用程序应该准备好执行。

```

```



返回[入门](https://gazebosim.org/docs/all/getstarted) 页面开始使用 Ignition！



Launch Gazebo by running:

```
gz sim shapes.sdf  # Fortress and Citadel use "ign gazebo" instead of "gz sim"
```



## 卸载二进制安装[![img](https://gazebosim.org/assets/icon/baseline-link-24px.svg)](https://gazebosim.org/docs/fortress/install_ubuntu#uninstalling-binary-install)

如果您在从二进制文件安装库后需要卸载 Ignition 或切换到基于源的安装，请运行以下命令：

```
sudo apt remove ignition-fortress && sudo apt autoremove
```



```
# 安装gazebo ubuntu22.04 ros-humble
sudo apt-get install ros-${ROS_DISTRO}-ros-gz



sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install gz-harmonic
```



```


# gazebosim
https://github.com/gazebosim/gz-sim

https://gazebosim.org/api/sim/8/classgz_1_1sim_1_1systems_1_1MecanumDrive.html
```



[Gazebo中模拟一个简单的差动驱动机器人](http://fishros.org/doc/ros2/humble/dev/Tutorials/Advanced/Simulators/Gazebo/Gazebo.html)

```
# 启动模拟
ign gazebo -v 4 -r visualize_lidar.sdf

# 命令行检查Gazebo提供的主题
ign topic -l

# 安装ros_gz_bridge让仿真与ros2通信
sudo apt install ros-humble-ros-ign-bridge -y

# 启动一个从ROS到Gazebo的桥接器
source /opt/ros/humble/setup.bash
ros2 run ros_gz_bridge parameter_bridge /model/vehicle_blue/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist


# 使用ros2 topic pub向主题发送命令
ros2 topic pub /model/vehicle_blue/cmd_vel geometry_msgs/Twist "linear: { x: 0.1 }"

# 使用键盘向主题发送命令
source /opt/ros/humble/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/model/vehicle_blue/cmd_vel
```

