

群晖DS3622xs+洗白码

----------------------------------------------------

您购买的订单号：3428296383777242413请注意查收：
SN：219HSQRNRFYGD MAC1：9009D0048C92
为防止被官方验证，7.x的用户请使用全球区账号登录，6.x用户请忽略
全球区账号注册教程:https://www.ainas.cc:88/?p=572
群晖安装及洗白教程:https://www.ainas.cc:88/?page_id=8
引导文件及常用工具下载:https://www.ainas.cc:88/?page_id=2
查看黑群晖洗白是否成功:https://www.ainas.cc:88/?p=304
一年内SN出现问题可免费更换2次，24小时确认収货并且好坪的可免费更换3次。

-------------



安装指南

https://www.bilibili.com/video/BV1YV4y1X7ak/?spm_id_from=333.337.search-card.all.click&vd_source=2b0c041bc65a68cc5157104c2c43b256



群晖核显硬解转码

https://www.bilibili.com/video/BV1eT411D7zb/?spm_id_from=333.337.search-card.all.click&vd_source=2b0c041bc65a68cc5157104c2c43b256



```
# ls -l /dev/dri

# cat /sys/kernel/debug/dri/0/i915_frequency_info | grep HW
HW control enabled: yes
```



https://github.com/wjz304/arpl-i18n 中文arpl地址



## arpl自定义SataPortMap引导群晖DSM

在进行到Add/edit an cmdline item时进行以下额外操作，添加SataPortMap、DiskIdxMap



注意：如果使用SAS Expander扩展更多硬盘接口要设置如下图（方法由Redpill_CustomBuild群：不见Liao 提供）
板载8口后面sas直通卡串SAS Expander扩展卡扩展更多的硬盘则需要把后面的每个sata芯片都设置为6。

`SataPortMap 06666`
`DiskIDxMap  00080E141A`
`SasIdxMap	0`



## Active Backup for Busness 激活命令

```
http://10.10.10.18:5000/webapi/auth.cgi?api=SYNO.API.Auth&method=Login&version=1&account=用户名&passwd=密码

http://10.10.10.18:5000/webapi/entry.cgi?api=SYNO.ActiveBackup.Activation&method=set&version=1&activated=true&serial_number="序列号"

http://10.10.10.18:5000/webapi/entry.cgi?api=SYNO.ActiveBackup.Activation&method=get&version=1

```

第一步，安装 Active Backup for Business 套件 


第二步，打开ABB套件，发现需要激活 

打开，控制面板 - 信息中心 - 产品序列号，复制备用

第三步，在网页输入以下网址

http://群晖地址:5000/webapi/auth.cgi?api=SYNO.API.Auth&version=3&method=login&account=管理员用户名&passwd=密码&format= cookie

然后网页提示中有"success":ture字样就是OK了 ，如下：

{"data":{"did":"mIUcp9U-ufiZZrA1UFxgqZtESjSReW0dzK8pD-WPxjEjQ_Aes7qErf4CKGh_xxxx","sid":"QER6F14sdbhys7pX_E5_mWskZtkKak-91FobgL7F9acPCkXjQsUyxxxx"},"success":true}

然后，在网页中输入以下网址：

http://群晖地址:5000/webapi/entry.cgi?api=SYNO.ActiveBackup.Activation&method=set&version=1&activated=true&serial_number="序列号"

将网址中的地址和序列号替换。 
