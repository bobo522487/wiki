# Win11使用mklink转移C:\Users文件夹至非系统盘



### **一、激活Administrator账户**

点击Windows徽标，输入“计算机管理”，回车调出计算机管理界面。

右键Administrator账户，选择“属性”，将“账户已禁用”前面的勾**取消（下图是已禁用的状态，要实现的是启用该账户）**，即激活该账户。



### **二、使用Administrator账户转移Users文件夹**

Windows键+X，再按U，快捷键调出关机或注销选项卡，选择**注销当前账户**（注意，不是"切换用户"，不注销会导致一些配置文件仍然在被使用，而导致接下来的复制和删除操作没法顺利完成，原理参考文章[[6\]](https://zhuanlan.zhihu.com/p/601679172?utm_id=0#ref_6)）。而后在登陆界面左下角会出现Administrator账户，选中直接登录。

**2.1 复制C:\Users文件夹到目标位置**

管理员身份打开命令行窗口，目标位置以"D:\Users"为例，输入以下命令：

```doscon
robocopy "C:\Users" "D:\Users" /E /COPYALL /XJ /XD "C:\Users\Administrator"
```

其中robocopy语法的基本格式为：robocopy <source> <destination> [<file>[ ...]] [<options>]，对应上述命令解释如下：

- **基本参数**："C:\Users"为源目录的路径；"D:\Users"为目标目录的路径；
- **复制选项**：/E表示复制子目录（包括空目录）；/COPYALL复制所有文件信息（等效于 /COPY:DATSOU，详见/COPY）；
- **文件选择选项**：/XJ 排除交接点（通常默认会包含，关于交接点Junction的解释详见[[7\]](https://zhuanlan.zhihu.com/p/601679172?utm_id=0#ref_7)）；/XD "C:\Users\Administrator" 排除与指定的名称和路径匹配的目录（在win11中似乎Administrator不在Users文件夹下生成文件，但此处添加并无大碍）

有关robocopy命令的具体细节见官方网站[[8\]](https://zhuanlan.zhihu.com/p/601679172?utm_id=0#ref_8)。

**2.2 删除C:\Users文件夹**

继续在上述管理员CMD窗口输入以下命令：

```text
rmdir "C:\Users" /S /Q
```

其中rmdir语法的基本格式为：rmdir [<drive>:]<path> [/s [/q]]，对应上述命令解释如下：

- **基本参数**："C:\Users"指定要删除的目录的位置和名称；/S删除 (指定目录及其所有子目录的目录树，包括所有文件)；/Q指定安静模式，删除目录树时不提示确认（仅当指定 /s时**，**/q参数才有效）。

有关rmdir命令的具体细节见官方网站[[9\]](https://zhuanlan.zhihu.com/p/601679172?utm_id=0#ref_9)。

**此步骤记得查看C盘的Users文件夹是否彻底删除**，有时可能会因为打开资源管理器到该目录子文件夹下导致其实未完全删除。（如果还是未能彻底删除，可以进入安全模式或者PE等系统工具辅助删除，但前提是已经使用robocopy复制好users文件夹，防止操作失败）

**2.3 创建目录交接点**

继续在上述管理员CMD窗口输入以下命令：

```text
mklink /J "C:\Users" "D:\Users"
```

其中rmdir语法的基本格式为：mklink [[/d] | [/h] | [/j]] <link> <target>，对应上述命令解释如下：

- **基本参数**：/J创建目录链接（通过交接点的操作都会被系统映射到实际的目录上。有关链接种类的说明可参见[[7\]](https://zhuanlan.zhihu.com/p/601679172?utm_id=0#ref_7)）；"C:\Users"要创建链接的名称；"D:\Users"新链接引用的路径。

有关mklink命令的具体细节见官方网站[[10\]](https://zhuanlan.zhihu.com/p/601679172?utm_id=0#ref_10)。

### **三、切回原账户并禁用Administrator账户**