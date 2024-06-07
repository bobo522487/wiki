### 修改IP地址

```yaml
vim /etc/netplan/00-installer-config.yaml
# This is the network config written by 'subiquity'
network:
  ethernets:
    ens192:	#你实际网卡地址
      addresses:
      - 10.10.10.40/24
      gateway4: 10.10.10.2
      nameservers:
        addresses:
        - 114.114.114.114
        search: []
  version: 2

```

### 修改主机名

```
hostnamectl set-hostname [YOUR NEW HOSTNAME]
```

### ssh登录

```yaml
#生成密匙对
ssh-keygen -t rsa -C "bobo522487@gmail.com"

#将本机公钥复制到服务器上
ssh-copy-id -i /root/.ssh/id_rsa.pub  root@10.10.10.xx

```

### 设置域名解析

```
cat > /etc/hosts <<EOF
10.10.10.30 k8s-kubeapi.t-plus.com.cn k8s-kubeapi
10.10.10.31 k8s-master1.t-plus.com.cn k8s-master1
10.10.10.32 k8s-master2.t-plus.com.cn k8s-master2
10.10.10.33 k8s-master3.t-plus.com.cn k8s-master3
10.10.10.34 k8s-node1.t-plus.com.cn k8s-node1
10.10.10.35 k8s-node2.t-plus.com.cn k8s-node2
10.10.10.36 k8s-node3.t-plus.com.cn k8s-node3
10.10.10.38 k8s-ha1.t-plus.com.cn k8s-ha1
10.10.10.39 k8s-ha2.t-plus.com.cn k8s-ha2
EOF

for i in {32..39};do scp /etc/hosts 10.10.10.$i:/etc/ ;done
```

### 禁用swap

```
swapoff -a
sed -i '/swap/s/^/#/' /etc/fstab
```

### 安装docker

```
apt-get -y install docker.io

# 修改cgroupdriver
cat > /etc/docker/daemon.json <<EOF
{
"exec-opts":["native.cgroupdriver=systemd"]
}
EOF
```

### 安装kubelet kubeadm kubectl

```
apt-get install -y kubelet kubeadm kubectl
```

### 安装cri-dockerd

```
curl -LO https://github.com/mirantis/cri-dockerd/release/download/v0.2.5/cri-dockerd_0.2.6.3-0.ubuntu-focal_amd64.deb

dpkg -i cri-dockerd_0.2.6.3-0.ubuntu-focal_amd64.deb

for i in {32..39};do scp cri-dockerd_0.2.6.3-0.ubuntu-focal_amd64.deb 10.10.10.$i:;ssh 10.10.10.$i "dpkg -i cri-dockerd_0.2.6.3-0.ubuntu-focal_amd64.deb";done
```



1. Update the `apt` package index and install packages needed to use the Kubernetes `apt` repository:

   ```shell
   sudo apt-get update
   sudo apt-get install -y apt-transport-https ca-certificates curl
   ```

2. Download the Google Cloud public signing key:

   ```shell
   sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
   ```

3. Add the Kubernetes `apt` repository:

   ```shell
   echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
   ```

4. Update `apt` package index, install kubelet, kubeadm and kubectl, and pin their version:

   ```shell
   sudo apt-get update
   sudo apt-get install -y kubelet kubeadm kubectl
   sudo apt-mark hold kubelet kubeadm kubectl
   ```



初始化

```
kubeadm init \
        --control-plane-endpoint="k8s-kubeapi.t-plus.com.cn" \
        --image-repository registry.cn-hangzhou.aliyuncs.com/google_containers \
        --cri-socket unix:///run/cri-dockerd.sock \
 		--pod-network-cidr=10.244.0.0/16 \
 		--service-cidr=10.96.0.0/12

```

安装网络插件

```shell
kubectl apply -f https://raw.githubusercontent.com/flannel-io/flannel/master/Documentation/kube-flannel.yml
```

