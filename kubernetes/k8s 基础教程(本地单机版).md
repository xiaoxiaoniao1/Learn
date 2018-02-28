# K8S 集群的介绍、安装与配置（实践版）

k8s 集群由一个 master 节点与多个 node 节点组成，所有节点均是在逻辑上独立的一个机器 。master 节点是管理整个集群的节点，而 node 节点是具体执行业务的节点，每个 node 都有一个 kubelet 作为其代理用于与 master 通信。

![enter image description here](https://d33wubrfki0l68.cloudfront.net/99d9808dcbf2880a996ed50d308a186b5900cec9/40b94/docs/tutorials/kubernetes-basics/public/images/module_01_cluster.svg)

而在本教程中，我们介绍 k8s 集群的基本操作：将会在本地机器上部署一个**单 Node 的 k8s 集群**，并尝试在该集群上**部署一个应用**、**配置暴露应用的服务**、以及**对应用进行规模调整与版本更新**。

### 术语简介

[kubectl](https://kubernetes.io/docs/reference/generated/kubectl/kubectl/) 是 k8s 的命令行管理工具，管理 k8s 集群需要通过该系列命令进行。

 [Minikube](https://kubernetes.io/docs/getting-started-guides/minikube/) 是一个用于在本地上运行 kubernates 的工具插件。Minikube 可在本地机器上创建一个虚拟机（需要安装对应的虚拟机驱动，如 VirtualBox、KVM 等），从而运行一个单节点的 k8s 集群。原理图如下：

![minikube 原理说明图](https://yqfile.alicdn.com/c03a43e0731ca579d1844fb44269fd2fd257bfb3.jpeg)

[VirtualBox](https://www.virtualbox.org/) 是一款支持 x86 和 AMD64/Intel64 的开源虚拟机软件，支持 Window、Linux 等系统。在本教程中，我们把它作为 Minikube 的虚拟机驱动。

## 1.  事前准备

- 准备好一台操作系统为 Linux CentOS 7 系统、内存为 **4G 以上**的虚机（或物理机），完成换源与关闭防火墙和 SELinux
- 需要在虚机上安装 VirtualBox 或 KVM 作为虚拟化软件（本教程介绍 VirtualBox 的安装）
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

> 在 Linux 下，Minikube 也支持 --vm-driver=none 选项来在本机运行 Kubernetes 组件（此种方式尚未实验）。

## 4. 使用 Minikube 运行集群

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

使用 `kubectl version` 可查看当前的 k8s 集群的客户端与服务端的版本；使用 `kubectl cluster-info` 可查看集群的详细部署情况；使用 `kubectl get nodes` 查看集群节点情况。

## 5. 在集群上部署应用

部署文件（Deployment）是用于指导 k8s 集群如何创建与维护应用实例的。

![enter image description here](https://d33wubrfki0l68.cloudfront.net/152c845f25df8e69dd24dd7b0836a289747e258a/4a1d2/docs/tutorials/kubernetes-basics/public/images/module_02_first_app.svg)

`kubectl run` 命令用于创建一个新的 Deployment，此命令需要提供 Deployment 的命名以及 app 镜像的地址。
```
# 若需要在特定端口运行app，则用 --port 指明运行端口
$ kubectl run kubernetes-bootcamp --image=docker.io/jocatalin/kubernetes-bootcamp:v1 --port=8080
# 创建完成后可以查询 Deployment
$ kubectl get deployments
```

Pod 是 k8s 集群管理的基本单位。当一个 Deployment 创建后，集群将会创建一个 Pod 来管理应用实例。一个 Pod 是一个 k8s 抽象，代表了一组（一个或多个）应用容器，且这些容器之间共享存储、网络等资源。

默认情况下，集群中的 Pods 对外部网络是不可见的，但 kubectl 可以创建一个能够转发请求到集群端私有网络的代理：`kubectl proxy`，执行后的输出类似如下（注意当前终端会阻塞）：
```
$ kubectl proxy
Starting to serve on 127.0.0.1:8001
```
通过使用 `kubectl proxy` 所展示的地址，我们就可以直接访问 k8s API，例如 `curl http://127.0.0.1:8001/version` 就可获取当前 API Server 的版本。

API Server 会自动根据 pod 的名字来为每个 pod 创建一个访问点（endpoint），该访问点也可以通过 proxy 来直接访问：
```
$ export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
$ echo Name of the Pod: $POD_NAME
$ curl http://localhost:8001/api/v1/proxy/namespaces/default/pods/$POD_NAME/
```

## 6. 查看 Pod 与 Node

一个 Pod 运行于一个 Node 上，Node 则是 k8s 集群中的执行业务的逻辑主机（虚拟机或者物理机），由 master 进行管理。一个 Node 可以拥有多个 Pod，且 master 可以在集群中的多个 node 之间自动调度 Pod。示意图如下：

![enter image description here](https://d33wubrfki0l68.cloudfront.net/5cb72d407cbe2755e581b6de757e0d81760d5b86/a9df9/docs/tutorials/kubernetes-basics/public/images/module_03_nodes.svg)

常用的查询应用的命令包括：
- **kubectl get** ： 列出资源
- **kubectl describe** : 展示资源详情
- **kubectl logs** : 打印某个 Pod 中的一个容器的日志
- **kubectl exec** : 在一个 Pod 中的一个容器中执行命令

## 7. 部署 Service

一个 Service 是集群中的一个抽象，它定义了一组逻辑相关的 Pods 以及如何访问它们的策略。Services 允许独立的 Pods 间的松耦合。

![enter image description here](https://d33wubrfki0l68.cloudfront.net/cc38b0f3c0fd94e66495e3a4198f2096cdecd3d5/ace10/docs/tutorials/kubernetes-basics/public/images/module_04_services.svg)

Service 使用标签（Label）和选择器（Selector）来匹配一组 Pods。

![enter image description here](https://d33wubrfki0l68.cloudfront.net/b964c59cdc1979dd4e1904c25f43745564ef6bee/f3351/docs/tutorials/kubernetes-basics/public/images/module_04_labels.svg)

尽管每个 Pod 都有自己独立的 IP，但是这些 IP 要是没有 Service 就无法被外部网络访问。Service 有以下配置模式：
- ClusterIP（默认）： 赋予 Service 一个集群内部 IP 。这种模式使得服务只能在集群内可被访问。
- NodePort：通过 NAT 允许 Service 使用集群内一个 Node 的 IP。从而就可以使用 \<NodeIP\>:\<NodePort\> 的方式让该 Service 可被集群外部访问。
- LoadBalancer：创建一个外部负载均衡器，并赋予 Service 一个固定的外部 IP。
- ExternalName：不使用代理，赋予 Service 一个任意的名字（由配置文件中的 `externalName` 参数决定）

以下命令可创建一个名为 “kubernetes-bootcamp” 的 NodePort 模式的 Service（其对外部网络可见）。再使用 `describe service` 命令可查看某个 Service 的详情：
```
$ kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080
$ kubectl describe services/kubernetes-bootcamp
```

可设置环境变量 NODE_PORT，通过 \<NodeIP\>:\<NodePort\> 从外网访问该 Service：
```
$ export NODE_PORT=$(kubectl get services/kubernetes-bootcamp -o go-template='{{(index .spec.ports 0).nodePort}}')
$ echo NODE_PORT=$NODE_PORT
$ curl host01:$NODE_PORT
```

接下来介绍 Label（标签）的使用。Deployment 会自动为 Pod 创建一个 Label，使用`kubectl describe`可以查看 Label 名字。使用带参的 `kubectl get` 命令可以查询特定 Label 的 Pod 或 Service。
```
$ kubectl get pods -l run=kubernetes-bootcamp
$ kubectl get services -l run=kubernetes-bootcamp
```

使用 `kubectl label` 命令为 Pod 增加一个新 Label 后，可用`kubectl describe`查询该 Pod 是否已有新 Label：
```
$ export POD_NAME=$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}')
$ echo Name of the Pod: $POD_NAME
$ kubectl label pod $POD_NAME app=v1
$ kubectl describe pods $POD_NAME
```

删除一个指定标签的 Service，之后便可测试到外部无法再通过 NodeIP 的方式访问到 app 了，但 app 仍在 Pod 中运行：
```
$ kubectl delete service -l run=kubernetes-bootcamp
$ curl host01:$NODE_PORT
$ kubectl exec -ti $POD_NAME curl localhost:8080
```

## 8. 调整应用规模

在之前的章节中，Deployment 只创建了一个 Pod 来运行应用，但当通信量增加时，就需要扩展应用数量来满足需求。实现的主要方式则是改变 Deployment 配置中的副本数量。应用规模变化的示意图如下：

![enter image description here](https://d33wubrfki0l68.cloudfront.net/043eb67914e9474e30a303553d5a4c6c7301f378/0d8f6/docs/tutorials/kubernetes-basics/public/images/module_05_scaling1.svg)

![enter image description here](https://d33wubrfki0l68.cloudfront.net/30f75140a581110443397192d70a4cdb37df7bfc/b5f56/docs/tutorials/kubernetes-basics/public/images/module_05_scaling2.svg)

若当前集群已有一个 Deployment（假设名为"kubernetes-bootcamp"），则可使用`kubectl scale`命令来扩展副本数量到 4 个，之后便可以检查到 pods 数量发生了变化。同时该变化也被 Deployment 记录到日志，可在详情中查看。
```
$ kubectl scale deployments/kubernetes-bootcamp --replicas=4
$ kubectl get deployments
$ kubectl get pods -o wide
$ kubectl describe deployments/kubernetes-bootcamp
```

## 9. 执行滚动更新

通常用户希望应用可一直被访问，而开发者希望应用可短时间内更新多次。而**滚动更新**能满足该要求，允许应用以零停机时间进行部署更新（通过新增的 Pods 来更新 Pods 实例）。默认情况下，更新过程中不可用 Pods 的最大数量与新创建 Pods 的最大数量相等。k8s 集群也可以回滚该更新。

![enter image description here](https://d33wubrfki0l68.cloudfront.net/678bcc3281bfcc588e87c73ffdc73c7a8380aca9/703a2/docs/tutorials/kubernetes-basics/public/images/module_06_rollingupdates2.svg)

![enter image description here](https://d33wubrfki0l68.cloudfront.net/9b57c000ea41aca21842da9e1d596cf22f1b9561/91786/docs/tutorials/kubernetes-basics/public/images/module_06_rollingupdates3.svg)

![enter image description here](https://d33wubrfki0l68.cloudfront.net/6d8bc1ebb4dc67051242bc828d3ae849dbeedb93/fbfa8/docs/tutorials/kubernetes-basics/public/images/module_06_rollingupdates4.svg)

使用`set image`命令可进行镜像更新，`rollout status`命令可进行更新确认提交，`rollout undo`可进行更新回滚。
```
$ kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=jocatalin/kubernetes-bootcamp:v2
$ kubectl rollout status deployments/kubernetes-bootcamp
$ kubectl rollout undo deployments/kubernetes-bootcamp
```

## 注意事项

1. 机器的内存必须在4G以上，否则启动 VirtualBox 时会失败
2. 使用 curl 下载时，偶尔会因为网速问题无法下载成功。此时应当通过其他方式下载文件然后手动上传到系统中
3. 启动 minikube 时可能会存在 localkube 找不到对应文件的情况，这是因为 localkube 的镜像下载不成功。

## 参考资料

[Running Kubernetes Locally via Minikube](https://kubernetes.io/docs/getting-started-guides/minikube/#minikube-features)（来自官网）

[Minikube：使用 Kubernetes 进行本地开发](https://linux.cn/article-8847-1.html)
<!--stackedit_data:
eyJoaXN0b3J5IjpbOTQ2MjI4MjY5XX0=
-->