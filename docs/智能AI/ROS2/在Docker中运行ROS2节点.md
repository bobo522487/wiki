# 在 Docker 中运行 ROS 2 节点 



## 在单个 docker 容器中运行两个节点[](https://docs.ros.org/en/humble/How-To-Guides/Run-2-nodes-in-single-or-separate-docker-containers.html#run-two-nodes-in-a-single-docker-container)

拉取带有标签“humble-desktop”的 ROS docker 镜像。

```
docker pull osrf/ros:humble-desktop
```



以交互模式在容器中运行镜像。

```
$ docker run -it osrf/ros:humble-desktop
root@<container-id>:/#
```



`ros2`现在你最好的朋友是命令行帮助。

```
root@<container-id>:/# ros2 --help
```



例如列出所有已安装的软件包。

```
root@<container-id>:/# ros2 pkg list
(you will see a list of packages)
```



例如列出所有可执行文件：

```
root@<container-id>:/# ros2 pkg executables
(you will see a list of <package> <executable>)
```



从此容器中的包运行 2 个 C++ 节点（1 个主题订阅者`listener`，1 个主题发布者）的最小示例：`talker``demo_nodes_cpp`

```
ros2 run demo_nodes_cpp listener &
ros2 run demo_nodes_cpp talker
```



## 在两个单独的 docker 容器中运行两个节点[](https://docs.ros.org/en/humble/How-To-Guides/Run-2-nodes-in-single-or-separate-docker-containers.html#run-two-nodes-in-two-separate-docker-containers)

打开终端。以交互模式在容器中运行图像，并使用以下命令启动主题发布者（可`talker`从包中执行`demo_nodes_cpp`）：`ros2 run`

```
docker run -it --rm osrf/ros:humble-desktop ros2 run demo_nodes_cpp talker
```



打开第二个终端。以交互模式在容器中运行图像，并使用以下命令启动主题订阅者（可`listener`从包中执行`demo_nodes_cpp`）：`ros2 run`

```
docker run -it --rm osrf/ros:humble-desktop ros2 run demo_nodes_cpp listener
```



作为命令行调用的替代方法，您可以创建一个`docker-compose.yml`包含以下（最少）内容的文件（此处为版本 2）：

```
version: '2'

services:
  talker:
    image: osrf/ros:humble-desktop
    command: ros2 run demo_nodes_cpp talker
  listener:
    image: osrf/ros:humble-desktop
    command: ros2 run demo_nodes_cpp listener
    depends_on:
      - talker
```



要在同一目录中运行容器调用。您可以使用 关闭容器。`docker compose up``Ctrl+C`