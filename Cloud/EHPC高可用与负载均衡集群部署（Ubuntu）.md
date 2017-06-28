# EHPC负载均衡及高可用集群部署说明

## 一.物理架构及技术简介

使用 Haproxy + Keepalived + nfs 作为集群部署方式。其中一台或多台 Hapoxy 代理服务器作为集群负载均衡的调度前端，多个 web 服务节点、单个数据库节点（同时提供 nfs 文件共享存储）作为对外隐藏的集群后端。

### HAProxy 
HAProxy（High Available Proxy）是一款提供高可用性、负载均衡以及基于 TCP（第四层）和 HTTP（第七层）应用的代理软件。 HAProxy 配置简单、支持多达上万并发连接。其运行模型可使得它非常容易和无风险地集成到现有的架构中，并且同时可以保护 web 服务器不被暴露到网络上。

### Keepalived
Keepalived 是一款高可用软件，它的功能是基于 VRRP 协议、通过 IP 漂移实现服务的高可用：服务器集群共享一个虚拟 IP，同一时间只有一个服务器占有虚拟 IP 并对外提供服务。若该服务器不可用，则虚拟 IP 漂移至另一台服务器并对外提供服务。

### NFS
在 Web 服务中往往需要涉及到一些不储存在数据库中的文件资源（比如用户上传的图片、文件等），而在集群中，若每个节点都有独立的文件存储的话，会造成存储不一致的后果。因此解决方案是构建一个 NFS（Network File System）服务器专门提供服务器节点间的共享文件存储，这样服务器节点间的存储就可以保持一致性。


## 二.部署准备

准备四台虚机（Linux Ubuntu），分别作为前端代理（ ha1[10.182.15.46]）、服务节点（web1[10.182.15.51
]、web2[10.182.15.52]）、数据库节点（nfs1[10.182.15.50]）。所有节点均可访问外网，其中只有 ha1 拥有公网 IP。

> 此外还拥有一台备份节点，用于对数据库节点 nfs1 的数据库以及文件目录进行实时主从备份。

所有节点须设置好 hosts 互相解析：
```
#vi /etc/hosts
10.182.15.46    ha1
10.182.15.50    nfs1
10.182.15.51    web1
10.182.15.52    web2
```
以及更新好 apt-get 库：`apt-get update`

## 三.数据库节点配置

数据库节点为 nfs1，主要提供 NFS 与 MySQL 服务。

### NFS 服务配置
安装 NFS 服务`sudo apt-get install nfs-kernel-server`，并编辑配置文件（路径为`/etc/exports`），配置文件中的每一行表示设置一个共享目录以及有其访问权限的主机地址。

```
# 共享目录路径为“/home/share”，对 web1 与 web2 两台主机开放读写权限
/home/share   web1(rw,sync,no_root_squash) web2(rw,sync,no_root_squash) 
```

启动 NFS 服务：`service nfs-kernel-server start`后， NFS 客户端才可对共享目录进行挂载。

共享目录中放置 ehpc 的服务端项目文件，所有 web 服务节点将一起使用共享目录中的项目文件。

更多配置参数请参考 [NFS服务器配置文档](https://github.com/Zouzhp3/Learn/blob/master/Cloud/%E9%85%8D%E7%BD%AE%E9%9B%86%E7%BE%A4%E5%85%B1%E4%BA%AB%E6%96%87%E4%BB%B6%20NFS%20%E6%9C%8D%E5%8A%A1%E5%99%A8.md)。

### MySQL 服务配置
ubuntu 系统一般会自带 MySQL 5.5，因此无需再安装一遍。首先使用默认的 mysql root 账户进入 mysql 命令行，修改 root 默认密码，并创建一个拥有访问权限的普通用户。

按照以下步骤设置开放 MySQL 的远程访问权限：

- 保证远程访问的 mysql 用户的 host 为'%'而不是'localhost'
- `sudo vi /etc/mysql/my.cnf`，注释掉`bind-address = 127.0.0.1`
- 重启 mysql 服务

之后导入原数据库的 sql 脚本即可。

至此便完成了节点 nfs1 的配置。

## 四.Web服务节点配置
本集群拥有两个 web 服务节点 web1、web2，两个节点的部署操作完全一致。

先使用 pip 安装 virtualenv、gunicorn、gevent、supervisor 等软件并使用`apt-get install nfs-common​`安装 NFS 客户端。再把 nfs1 节点开放的共享目录`/home/share`挂载到本地目录`/home/haproxy/share`，并设置为永久挂载（挂载操作参考 [NFS服务器配置文档](https://github.com/Zouzhp3/Learn/blob/master/Cloud/%E9%85%8D%E7%BD%AE%E9%9B%86%E7%BE%A4%E5%85%B1%E4%BA%AB%E6%96%87%E4%BB%B6%20NFS%20%E6%9C%8D%E5%8A%A1%E5%99%A8.md)）。

迁移原 python 虚拟环境（迁移方法参考本文文末）后，还需要配置环境变量：把原脚本`.bashrc` copy 到用户根目录中，并对其中数据库配置等环境参数进行修改以满足当前实际要求，之后`source ~/.bashrc`刷新环境变量即可。

之后配置 supervisor（路径`/etc/supervisor/conf.d/ehpc.conf`）：
```
[program:ehpc]
command=/home/haproxy/env/bin/gunicorn manage:app -b 0.0.0.0:80 -w 4 --worker-class gevent
autostart = true
autorestart = true
user=root
```

> 注意 manage.py 路径，需当前工作目录为项目主目录才可启动成功。最好在启动 supervisor 前手工启动跑一下以便及早发现可能的问题。

## 五.HAProxy代理节点配置

前端节点为 ha1，作为集群中唯一直接对外通信的代理服务器。

安装 HAProxy：`yum install haproxy`，然后配置 HAProxy（路径`/etc/haproxy/haproxy.cfg`）。

HAProxy 的配置文件分为五个部分：

- global：全局配置的进程级参数，用来控制 Haproxy 启动前的一些进程及系统设置
- defaults：配置默认参数，可以被 frontend，backend，listen 段继承使用
- frontend：定义接收请求的前端虚拟节点，可根据用户所请求的不同域名、URL 等做不同的请求处理
- backend：定义处理业务的后端服务器集群，以及设置后端的权重、队列、连接数等选项
- listen：frontend 和 backend 的组合体

> 配置参数详细说明请查阅 [HAProxy用法详解](http://www.ttlsa.com/linux/haproxy-study-tutorial/)。

以下是 ha1 的配置实例：
```
global
        log /dev/log    local0
        log /dev/log    local1 notice
        chroot /var/lib/haproxy
        maxconn 20000
        daemon

defaults
        log     global
        mode    http
        option  httplog
        option  dontlognull
        option http-server-close
        option forwardfor except 127.0.0.0/8
        option redispatch
        retries 3             # 3次连接失败就认为服务器不可用
        timeout http-keep-alive 10s           # 默认持久连接超时时间
        timeout check           10s           # 心跳检查超时时间
        contimeout 5000
        clitimeout 50000
        srvtimeout 50000
        errorfile 400 /etc/haproxy/errors/400.http
        errorfile 403 /etc/haproxy/errors/403.http
        errorfile 408 /etc/haproxy/errors/408.http
        errorfile 500 /etc/haproxy/errors/500.http
        errorfile 502 /etc/haproxy/errors/502.http
        errorfile 503 /etc/haproxy/errors/503.http
        errorfile 504 /etc/haproxy/errors/504.http

frontend  proxy *:80    #前端代理
        default_backend  dynamic

backend dynamic    #后端Web服务器
        balance roundrobin
        cookie  SESSION_ID insert indirect nocache    #设置cookie保持
        server  web1  10.182.15.51:80 inter 3000 rise 2 fall 3 check maxconn 10000 cookie A
        server  web2  10.182.15.52:80 inter 3000 rise 2 fall 3 check maxconn 10000 cookie B
```

启动 HAProxy 服务：`service haproxy start`即可。

## 如何进行项目文件更新
更新之前先停掉 web1 与 web2 的服务：`supervisorctl stop ehpc`

- 更新数据库：登录 nfs1，进入 mysql 命令行进行新的数据库 sql 文件导入即可
- 更新项目文件：登录 nfs1，新的项目文件代替`/home/share`中对应的文件即可。

> 提示：由于通过跳板机登录 nfs1 不能使用 sftp 功能，因此目前也把跳板机下的目录挂载了 nfs1 上的共享目录，这样直接通过在跳板机上上传文件就可以修改项目文件了。

最后记得要重启 web1 与 web2 的服务：`supervisorctl start ehpc`

## 架构中将来可能遇到的问题
由于 nfs1 既作为集群中唯一的数据库服务节点以及唯一的文件共享目录挂载节点，同时还负责对外实时备份，因此很有可能成为集群中效率的瓶颈。今后的架构重构中，应当考虑把数据库服务从文件共享目录挂载节点分离开，减小 nfs1 的压力。

## 部署问题汇总

### ubuntu系统设置DNS失败
在`/etc/resolvconf/resolv.conf.d/base`里添加 DNS 失败，则应当在`/etc/resolvconf/resolv.conf.d/head`中进行添加，之后使用`resolvconf -u`刷新即可。

### 启动 80 端口的 web 节点的服务时提示端口被占用
ubuntu 系统自带 Apache2 服务占用了 80 端口且开机自动启动，用`sudo lsof -i:80`命令找出 80 端口的占用程序 kill 掉即可，此外还可使用`sudo update-rc.d apache2 disable`命令关闭 apache2 的自启动。

### virtualenv 虚拟环境迁移后无法正常引用库
直接 copy 虚拟环境到另一台主机上就会出现新虚拟环境下的 python 无法引用库的问题。解决方法是在新主机上重新新建一个虚拟环境，然后把要原虚拟环境中的`lib/python2.7/site-packages/`目录下的库都 copy 到新虚拟环境中的该目录下即可。

### 复制 .bashrc 文件后虚拟环境导向出错 
.bashrc 复制到新的主机的用户根目录下时出现，删除以下两行即可：
```
export WORKON_HOME=~/.Envs
source /usr/local/bin/virtualenvwrapper.sh
```

### 设置语言的环境变量时警告 warning: setlocale: LC_ALL： cannot change locale (zh_CN.UTF-8)
如果不处理的话会导致程序中编码问题而报错。这是因为系统里没有安装对应的语言包，使用`sudo apt-get install language-pack-zh-hans`安装对应的语言包后重启并`source ~/.bashrc`即可。

### 安装 gevent 失败
使用`pip install gevent`安装 gevent 时失败时，需要安装依赖包 python-dev ：`sudo apt-get install python-dev`

### supervisor启动后 web 服务启动失败
在使用 supervisor 启动服务前先使用`gunicorn manage:app -b 0.0.0.0:80 -w 4 --worker-class gevent`命令进行测试，观察服务能否正常启动。若测试成功，则还要保证以下三点：

- 工作目录是 ehpc 项目的主目录
- supervisor 服务处于开启状态：`sudo service supervisor status`
- 使用`supervisord -c /etc/supervisor/supervisor.conf`启动 supervisor 进程