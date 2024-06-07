

### 1、标定前准备

- 一个已知尺寸的大棋盘。本教程使用9x6棋盘格和20毫米正方形，标定的时候要展平。**校准使用棋盘格的内部顶点，因此“10x7”棋盘使用内部顶点参数“9x6”，如下例所示。**什么规格的标定板都可以，只不过改一下参数就好。空旷一点的区域，没有障碍物和标定板图案
- 通过 ROS 发布图像的单目相机

### 2、开始标定

安装标定的功能包camera_calibration，docker终端输入，

```
sudo apt install ros-foxy-camera-calibration*
```

在标定之前启动相机，直到全部标定完毕再关闭相机，启动相机（以启动astraproplus相机为例），Docker终端中输入，

```
ros2 launch astra_camera astro_pro_plus.launch.xml
```

使用以下命令查看话题，Docker终端中输入，

```
ros2 topic list
```

![image-20230426161443070](https://www.yahboom.com/public/upload/upload-html/1706083681/image-20230426161443070.png)

我们标定RGB彩色图像需要用到的话题是/camera/color/image_raw.

运行标定的程序，Docker终端中输入，

```
ros2 run camera_calibration cameracalibrator --size 8x6 --square 0.025 --ros-args --remap /image:=/camera/color/image_raw
```

size：标定棋盘格的内部角点个数，例如 8 X 6，角点一共六行八列。

square：棋盘格的边长，单位是米。

话题名字：/camera/color/image_raw，如果是启动**usb_cam**的话，这里修改成**/image_raw**

![image-20230426161833099](https://www.yahboom.com/public/upload/upload-html/1706083681/image-20230426161833099.png)

X：棋盘格在摄像头视野中的左右移动

Y：棋盘格在摄像头视野中的上下移动

Size ：棋盘格在摄像头视野中的前后移动

Skew：棋盘格在摄像头视野中的倾斜转动

如上图所示，需要通过上下前后左右左右翻转来采集图像，使得右边的X、Y、Size、Skew变成绿色，如下图所示，然后点击CALIBRATE，开始标定。

![image-20230426162103880](https://www.yahboom.com/public/upload/upload-html/1706083681/image-20230426162103880.png)

标定结束后，点击SAVE，如下图所示，

![image-20230426162241771](https://www.yahboom.com/public/upload/upload-html/1706083681/image-20230426162241771.png)

标定结果保存至【/tmp/calibrationdata.tar.gz】，保存的路径为标定程序启动的终端目录下。标定结束后，可以移动出来【/tmp/calibrationdata.tar.gz】文件看看内容

```
sudo mv /tmp/calibrationdata.tar.gz ~
```

docker终端输入，

```
cd ~
tar -xvf calibrationdata.tar.gz
```

会在终端目录下得到标定的png文件、ost.yaml和ost.txt文件

由于astra驱动启动的时候是加载代码里边标定好的内置的参数，所以不需要加载这个标定后的参数，但是当启动usb摄像头时是需要加载参数的，因此，标定后需要把参数替换原来的内置参数，把标定好的ost.yaml改名为camera_info.yaml，然后替换原来的camera_info.yaml，docker终端输入，

```
#先把文件复制到/opt/ros/foxy/share/usb_cam/config
sudo cp ost.yaml /opt/ros/foxy/share/usb_cam/config
#切换至/opt/ros/foxy/share/usb_cam/config目录下
cd /opt/ros/foxy/share/usb_cam/config
#备份原来的camera_info.yaml
sudo mv camera_info.yaml camera_info_BK.yaml
#重命名ost.yaml为camera_info.yaml
sudo mv ost.yaml camera_info.yaml
```

 