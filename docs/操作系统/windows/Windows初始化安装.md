## 创建VHD并安装Windows系统

### 创建VHD

```
启动wePE
打开DiskGenius
删除硬盘所有分区，保存更改；
右键创建ESP、MSR分区，默认设置（大小是否由300改为1024）；
剩下的空间新建NTFS主磁盘分区，扇区选择 4096，保存更改；

将镜像文件、驱动复制到C盘
将windows镜像加载到光驱

运行WinNTSetup,
  选择Windows安装源: D:\sources\install.wim
  选择引导驱动器： Z:
  创建 VHD>>> , 位置 C:\vhdx\win11.vhdx，大小120 VHDX GB，分配单元大小4096，动态扩展
  选择安装驱动器： 选择刚创建挂载的分区，例如W：
  选项： 选择windows 11 专业版
  开始安装，确定，重启；
  
```

### windows安装激活命令

```
slmgr /ipk NRG8B-VKK3Q-CXVCJ-9G2XF-6Q84J
slmgr /skms kms.loli.best
slmgr /ato
```

#跳过微软账户登录，shift+F10输入一下命令重启

```
oobe\bypassnro.cmd
```

### 用户主目录转移

```
@echo off
robocopy "C:\\Users" "D:\\Users" /E /COPYALL /XJ /XD WindowsApps
rmdir "C:\\Users" /S /Q
mklink /J "C:\\Users" "D:\\Users"
```


上面的内容保存为 mv.bat 保存到D盘。
开始运行或徽标+R
shutdown -O -r -t 0
重启到恢复界面

进入疑难问题菜单-命令提示符

```
CD D:
mv.bat
```

执行MV.bat 即可.





### 建立差分系统

```
运行BOOTICE
选择镜像文件 C:\vhdx\win11.vhdx
子文件位置输入 C:\vhdx\win11_daily.vhdx
点击创建；

同理创建 win11_game.vhdx，win11_crypto.vhdx，win11_solidworks.vhdx...
```

### 备份差分系统

```
创建 C:\vhdx\vhdx_backup 文件夹
将所有 vhdx文件复制到 vhdx_backup 文件夹
```

### 修改引导

```
创建 C:\vhdx\ESP\ESP_original 文件夹
打开DiskGenius，找到ESP分区，点击浏览文件，选中Boot和EFI文件夹，右键 复制到指定文件夹 C:\vhdx\ESP\ESP_original
强制删除原Boot和EFI文件夹
复制 C:\vhdx\ESP\ESP_original下的Boot和EFI文件夹到上一级目录C:\vhdx\ESP
```

### 编辑启动项

```
运行 BOOTICE / BCD编辑
选中其他BCD文件，选择 C:\vhdx\ESP\EFI\Microsoft\Boot\BCD 文件，点击智能编辑模式；
删除已有引导项；

添加引导
-------
设备类型： VHD（X）
启动磁盘： C盘
启动分区： C盘
设备文件: \vhdx\win11_daily.vhdx
菜单标题： Windows11 for Daily
NX: OptIn
检测硬件抽象层 选中 			启动到WinPE 禁用
启用Win8 Metro启动界面 选中  测试模式 禁用
超时时间 5
点击保存当前系统设置，保存全局设置；

同理添加 win11_game.vhdx，win11_crypto.vhdx，win11_solidworks.vhdx...

```

