# 在 Debian 上安装 Docker 引擎

要在 Debian 上开始使用 Docker Engine，请确保 [满足先决条件](https://docs.docker.com/engine/install/debian/#prerequisites)，然后按照 [安装步骤](https://docs.docker.com/engine/install/debian/#installation-methods)进行操作。

### [使用便捷脚本安装](https://docs.docker.com/engine/install/debian/#install-using-the-convenience-script)



```console
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

您现在已经成功安装并启动了 Docker Engine。该`docker` 服务在基于 Debian 的发行版上自动启动。在`RPM`CentOS、Fedora、RHEL 或 SLES 等基础发行版上，您需要使用适当的`systemctl`或`service`命令手动启动它。正如消息所示，默认情况下非 root 用户无法运行 Docker 命令。

> **以非特权用户身份使用 Docker，还是以无根模式安装？**
>
> 安装脚本需要安装和使用 Docker 的权限`root`。`sudo`如果您想授予非 root 用户访问 Docker 的权限，请参阅 [Linux 的安装后步骤](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)。您还可以在没有`root`特权的情况下安装 Docker，或配置为在无根模式下运行。有关在 rootless 模式下运行 Docker 的说明，请参阅 [以非 root 用户身份运行 Docker 守护进程（rootless 模式）](https://docs.docker.com/engine/security/rootless/)。



要创建`docker`组并添加您的用户：

1. 创建`docker`群组。

   ```console
   $ sudo groupadd docker
   ```

2. 将您的用户添加到`docker`组中。

   ```console
   sudo usermod -aG docker $USER
   ```

3. 注销并重新登录，以便重新评估您的组成员身份。

   > 如果您在虚拟机中运行 Linux，则可能需要重新启动虚拟机才能使更改生效。

   您还可以运行以下命令来激活对组的更改：

   ```console
   newgrp docker
   ```

4. 验证您是否可以`docker`在没有`sudo`.

   ```console
   $ docker run hello-world
   ```

   此命令下载测试映像并在容器中运行它。当容器运行时，它会打印一条消息并退出。



## [卸载 Docker 引擎](https://docs.docker.com/engine/install/debian/#uninstall-docker-engine)

1. 卸载 Docker Engine、CLI、containerd 和 Docker Compose 软件包：

   

   ```console
   $ sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
   ```

2. 主机上的映像、容器、卷或自定义配置文件不会自动删除。要删除所有映像、容器和卷：

   

   ```console
   $ sudo rm -rf /var/lib/docker
   $ sudo rm -rf /var/lib/containerd
   ```

您必须手动删除任何编辑的配置文件。