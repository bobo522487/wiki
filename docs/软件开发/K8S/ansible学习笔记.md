1 安装
sudo pip install ansible


2 配置
2.1 管理服务器：inventory文件
  通常命名为hosts文件，可以加标签分组，可以使用 1:N等通配符等；

2.2 ansible.cfg文件
vi /etc/ansible/ansible.cfg
#建议取消注释 host_key_checking = false
#建议取消注释 log_path = /var/log/ansible.log

-------------------------
hostname ansible	#修改主机名
sudo vi /etc/netplan/00-installer-config.yaml	#设置固定IP

vi /etc/ssh/sshd_config		#配置ssh
systemctl restart sshd
-------------------------




2 批量推送公钥

ssh-keygen
ssh-copy-id  10.10.10.?  #分别执行多台机器的IP

#或者编写剧本
- hosts: all
  user: root
  tasks:
   - name: ssh-copy
     authorized_key: user=root key="{{ lookup('file', '/home/root/.ssh/id_rsa.pub') }}"
     tags:
       - sshkey

3 模块（Modules）

-apt 
这个模块是ubuntu和Debian作为远端节点的时候用的最多的包管理工具
  deb: 软件包名字，可选
  install_recommends: 默认为true，设置为False代表只下载不安装
  update_cache: yes相当于apt-get update
  name: apt要下载的软件名，指定版本可用name=git=1.6
  state: (present, adsent, latest) present表示为安装，然后是删除，再是安装位最新版本

-copy 
在远程主机上面复制文件
  src: 复制到远程的文件在本地的地址，如果路径以/结尾，只复制目录里面的内容，如果没有，则包含目录在内的整个内容全部复制
  content: 代替src，可以直接设定指定文件的值
  dest: 复制到远程文件的路径
  directory_mode: 目录权限
  force:默认为yes，强制覆盖
  others: 所有file模块里面的选项
  mode: 0644

-synchronize 
使用rsync同步文件，将主控方目录推送到指定节点的目录下
  delete: 删除不存在的文件
  src: 要同步到目的地的源主机的路径
  dest: 目的地上同步地址
  dest_port: 目的地机上的端口
  mode: push/pull，默认push，本机向远程传文件
  rsync_opts:
ansible 10.10.10.231 -m synchronize -a 'mode=pull  src=/root/chia-blockchain/venv dest=/root/ compress=yes'

-service
  arguments: 命令选项
  enabled: 是否开机启动 yes
  name: 必选，服务名称
  runlevel: 运行级别
  sleep: restarted之间的间隔
  state: started/stopped/restarted/reloaded

-get_url
用于从http，ftp，https服务器上面上下载文件，类似wget
  sha256sum: 下载后sha256验证
  timeout: 下载超时时间，默认为10s
  url: 下载的url
  url_password, url_username: 如果下载需要提供验证
  dest: 下载到哪里
  headers: 以key:value的格式自定义http标头

-file
用于远程主机上面的文件操作
  force: 强制创建软连接
  group: 文件目录的属组
  mode: 文件目录的权限
  owner: 文件目录的属主
  path: 必选，文件目录的路径
  recurse: 递归的设置文件的属性
  src: 被连接的源文件路径，当state=link的时候
  dest: 被连接到的路径，当state=link的时候
  state: directory 如果目录不存在则创建目录
  file 如果文件不存在则创建
  link 创建软连接
  hard 创建硬链接
  touch 如果文件不存在则创建，如果存在则修改最后修改时间属性
  absent 删除文件目录或者取消连接文件


4 剧本（Playbooks）
---
# hosts could have been "remote" or "all" as well
- hosts: local
  connection: local
  become: yes
  become_user: root
  tasks:
   - name: Install Nginx
     apt:
       name: nginx
       state: installed
       update_cache: true



###############################################
crontab -l  查看
crontab -e  编辑

tar -cvf bdir.tar bdir  #打包
tar -xzvf bdir.tar      #解压到当前目录下

screen -X -S ID quit   删除screen


ansible 10.10.10.231 -m synchronize -a 'src=/root/.chia/mainnet/ dest=/root/.chia/

ansible localhost -m cron -a 'name="auto ploti" minute=* hour=*/1 day=* month=* weekday=* job="bash /home/start.sh"' 
ansible localhost -m cron -a 'name="auto move plots" minute=*/30 hour=* day=* month=* weekday=* job="\mv /mnt/d/chia_final/*.plot /mnt/e/"'