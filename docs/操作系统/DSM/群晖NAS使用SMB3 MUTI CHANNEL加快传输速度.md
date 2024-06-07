## 群晖NAS使用SMB3 MUTI CHANNEL加快传输速度



需要所用到的设备：

1. 双网口群晖
2. 带有两个网卡的PC（普通计算机可以加一块PCI-E网卡）
3. 带有至少4个口的交换机
4. 四根千兆网线（CAT6）

## STEP1

群晖DSM中没有直接修改SMB3 muti channel的选项，需要修改smb.conf文件。通过ssh以root登陆群晖。samba配置文件路径/etc/samba/smb.conf。用以下命令找到：

```
sudo vi /etc/samba/smb.conf
```

添加以下命令，保存后重启。

```
    server multi channel support = yes
    aio read size = 1
    aio write size = 1
```

## STEP2

群晖控制台WEB界面，控制面板–文件共享–文件服务–高级设置：
最大SMB协议：SMB3
最小SMB协议：SMB2和Large MTU
设置完毕，点应用。然后设置就完成。
![在这里插入图片描述](https://www.freesion.com/images/286/50f743c8f02c8439c55eed46f0416456.png)

## STEP3 验证

以管理员身份启动CMD，然后在里面输入,看到双通道说明成功

```
PowerShell
Get-SmbMultichannelConnection

```

![在这里插入图片描述](https://www.freesion.com/images/209/450895d9a96258291fd04ab1b4323b79.png)看到以上显示说明已经设置成功。尝试复制NAS文件。



windows11网卡-》高级

```
RSS队列的最大数目    16
流量控制			禁用
传输缓冲区			4096
接收缓冲区			4096

```

