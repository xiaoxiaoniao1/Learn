# 本地单机版K8S集群的安装与配置

 [Minikube](https://kubernetes.io/docs/getting-started-guides/minikube/) 是一个用于在本地上运行 kubernates 的工具插件。Minikube 可在本地机器上创建一个虚拟机（需要安装对应的虚拟机驱动，如 VirtualBox、KVM 等），从而运行一个单节点的 k8s 集群。

![minikube 原理说明图](https://yqfile.alicdn.com/c03a43e0731ca579d1844fb44269fd2fd257bfb3.jpeg)

[kubectl](https://kubernetes.io/docs/reference/generated/kubectl/kubectl/) 则是 k8s 的命令行管理工具，管理 k8s 集群需要通过该系列命令进行。

## 1.  事前准备

- 准备好一台操作系统为 Linux CentOS 7 系统、内存为 **4G 以上**的虚机（或物理机），完成换源与关闭防火墙和 SELinux
- 需要在虚机上安装 VirtualBox 或 KVM 作为虚拟化软件（本教程将会介绍 VirtualBox 的安装）
- 设置 CPU 支持虚拟化 VT-X（若是物理机则在BIOS上设置，若是虚机则在VMware里设置 ）

## 2. 配置 kubectl 与 Minikube

下载 kubectl 并配置到系统路径：
```
$ curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.9.1/bin/linux/amd64/kubectl
$ chmod +x ./kubectl
$ sudo mv ./kubectl /usr/local/bin/
```

> 注意 kubectl 的版本必须新于 k8s 服务器的版本，否则会出现校验错误。可通过 `curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt` 命令查询当前的最新稳定版本。

下载 Minikube 并配置到系统路径：
```
$ curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 
$ chmod +x ./minikube
$ sudo mv ./minikube /usr/local/bin/
```

> 注意：由于本节所述的下载网址有时会无法通过 curl 命令访问，因此建议直接下载 kubectl 或 minikube 到本地再上传到虚机中。也可以通过其他途径如 [minikube 的 github 下载地址](https://github.com/kubernetes/minikube/releases) 进行下载。

## 3. 安装 VirtualBox

本教程中 minikube 的虚拟机采用 VirtualBox ，安装步骤如下：
1. 在官网下载对应系统的 VirtualBox rpm 包
2. 安装 VirtualBox 的依赖包：`yum install qt qt-x11 gcc gcc-c++ kernel-devel perl SDL`
3. 安装 VirtualBox：`rpm -i VirtualBox-5.2-5.2.6_120293_el7-1.x86_64.rpm`
4. 添加当前用户到 VirtualBox 创建的用户组 "vboxusers"：`usermod -a -G vboxusers {{用户名}}`

> Minikube 也支持 --vm-driver=none 选项来在本机运行 Kubernetes 组件，这时候需要本机安装了 Docker （此种方式尚未实验）。

## 4. 运行 Minikube

执行 `minikube start` 启动本地 k8s 集群。当正常启动成功时，出现以下输出：
```
Starting local Kubernetes v1.8.0 cluster...
Starting VM...
Downloading Minikube ISO
 140.01 MB / 140.01 MB [============================================] 100.00% 0s
Getting VM IP address...
Moving files into cluster...
Downloading localkube binary
 148.25 MB / 148.25 MB [============================================] 100.00% 0s
Connecting to cluster...
Setting up kubeconfig...
Starting cluster components...
Kubectl is now configured to use the cluster.
Loading cached images from config file.
```
执行 `minikube status` 可查看当前集群状态，输出类似如下所示：
```
minikube: Running
cluster: Running
kubectl: Correctly Configured: pointing to minikube-vm at 192.168.99.100
```

## 5. 集群的运行与测试

执行 `minikube start` 命令而启动本地 k8s 集群后，使用 `kubectl version` 可查看当前的 k8s 集群的客户端与服务端的版本；使用 `kubectl cluster-info` 可查看集群的详细部署情况；使用 `kubectl get nodes` 查看集群节点情况。



## 注意事项
1. 机器的内存必须在4G以上，否则启动 VirtualBox 时会失败
2. 使用 curl 下载时，偶尔会因为网速问题无法下载成功。此时应当通过其他方式下载文件然后手动上传到系统中
3. 启动 minikube 时可能会存在 localkube 找不到对应文件的情况，这是因为 localkube 的镜像下载不成功。

## 参考资料
[Running Kubernetes Locally via Minikube](https://kubernetes.io/docs/getting-started-guides/minikube/#minikube-features)（来自官网）
[Minikube：使用 Kubernetes 进行本地开发](https://linux.cn/article-8847-1.html)
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTgwMjc2NDM5M119
-->