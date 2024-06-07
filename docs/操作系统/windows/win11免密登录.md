

### win11免密登录

任务栏放大镜搜索:“注册表编辑器”，管理员方式打开

依次找到:

```
计算机\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\PasswordLess\Device
```

原始值是2，双击改成0即可！

2、然后在“运行”里输入：

netplwiz

去掉对勾