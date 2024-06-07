

# 入门[](https://moveit.picknik.ai/humble/doc/tutorials/getting_started/getting_started.html#getting-started)

在这里，我们将设置您的环境，以便最好地运行教程。这将创建一个 Colcon 工作区，下载所有最新的 MoveIt 源代码，并从源代码构建所有内容，以确保您拥有最新的修复和改进。

构建 MoveIt 的所有源代码可能需要 20-30 分钟，具体取决于计算机的 CPU 速度和可用 RAM。如果您使用的是性能较差的系统，或者通常只是想更快地入门，请查看我们的[Docker 指南](https://moveit.picknik.ai/humble/doc/how_to_guides/how_to_setup_docker_containers_in_ubuntu.html)。

## 一键安装 ROS 2 和 Colcon[](https://moveit.picknik.ai/humble/doc/tutorials/getting_started/getting_started.html#install-ros-2-and-colcon)

```
wget http://fishros.com/install -O fishros && . fishros
```



## 创建 Colcon 工作区并下载教程[](https://moveit.picknik.ai/humble/doc/tutorials/getting_started/getting_started.html#create-a-colcon-workspace-and-download-tutorials)

对于教程，您需要有一个[colcon](https://docs.ros.org/en/rolling/Tutorials/Colcon-Tutorial.html#install-colcon)工作区设置。

```
mkdir -p /home/bobo/ws_moveit2/src
```



## 下载MoveIt源代码和教程[](https://moveit.picknik.ai/humble/doc/tutorials/getting_started/getting_started.html#download-source-code-of-moveit-and-the-tutorials)

进入 Colcon 工作区并提取 MoveIt 教程源：

```
cd /home/bobo/ws_moveit/src
git clone --branch humble https://github.com/ros-planning/moveit2_tutorials
```



接下来我们将下载 MoveIt 其余部分的源代码：

```
vcs import < moveit2_tutorials/moveit2_tutorials.repos
```



## 构建您的 Colcon 工作空间[](https://moveit.picknik.ai/humble/doc/tutorials/getting_started/getting_started.html#build-your-colcon-workspace)

以下将从 Debian 安装工作区中尚未存在的任何软件包依赖项。这是安装 MoveIt 及其所有依赖项的步骤：

```
sudo apt update && rosdep install -r --from-paths . --ignore-src --rosdistro $ROS_DISTRO -y
```



下一个命令将配置您的 Colcon 工作区：

```
cd /home/bobo/ws_moveit
colcon build --mixin release
```



此构建命令可能需要很长时间（20 分钟以上），具体取决于您的计算机速度和可用 RAM 量（我们建议 32 GB）。如果您的计算机内存不足或者通常您的构建难以在计算机上完成，您可以将该参数附加到上面的 colcon 命令中。`--parallel-workers 1`

如果一切顺利，您应该看到“完成”消息。如果您遇到问题，请尝试重新检查您的[ROS Installation](https://docs.ros.org/en/humble/Installation.html)。

## 设置您的 Colcon 工作区[](https://moveit.picknik.ai/humble/doc/tutorials/getting_started/getting_started.html#setup-your-colcon-workspace)

获取 Colcon 工作区：

```
source /home/bobo/ws_moveit/install/setup.bash
```



可选：将前面的命令添加到您的`.bashrc`：

```
echo 'source /home/bobo/ws_moveit/install/setup.bash' >> ~/.bashrc
```





## 切换到 Cyclone DDS[](https://moveit.picknik.ai/humble/doc/tutorials/getting_started/getting_started.html#switch-to-cyclone-dds)

截至 2022 年 9 月 26 日，默认的 ROS 2 中间件 (RMW) 实现存在问题。作为解决方法，请切换到 Cyclone DDS。 （注意：这使得使用此 RMW 启动的所有节点与不使用 Cyclone DDS 的任何其他节点不兼容。）

```
sudo apt install ros-humble-rmw-cyclonedds-cpp
# You may want to add this to ~/.bashrc to source it automatically
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
```