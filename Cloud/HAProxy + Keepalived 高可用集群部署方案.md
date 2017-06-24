# 技术简介

### HAProxy 

HAProxy（High Available Proxy）是一款提供高可用性、负载均衡以及基于 TCP（第四层）和 HTTP（第七层）应用的代理软件。 HAProxy 配置简单、支持多达上万并发连接。其运行模型可使得它非常容易和无风险地集成到现有的架构中，并且同时可以保护 web 服务器不被暴露到网络上。

### Keepalived
Keepalived 是一款高可用软件，它的功能是基于 VRRP 协议，通过 IP 漂移实现服务的高可用：服务器集群共享一个虚拟 IP，同一时间只有一个服务器占有虚拟 IP 并对外提供服务。若该服务器不可用，则虚拟 IP 漂移至另一台服务器并对外提供服务。

Keepalived 可以单独使用，即通过 IP 漂移实现服务的高可用，也可以结合 LVS 使用（即一方面通过 IP 漂移实现 LVS 负载均衡层的高可用，另一方面实现 LVS 应用服务层的状态监控）。


# HAProxy + Keepalived 部署方案

准备四台虚机，分别记作 HA-master、HA-slave、web-node1、web-node2。前两者作为 HA 负载均衡调度器（即前端），后两者是提供应用服务的 web 服务器（即后端）。

## 前端配置

### 前端配置 keepalived
HA-master 与 HA-slave 都需安装 keepalived 服务：`yum -y install keepalived`，keepalived 的配置文件路径为`/etc/keepalived/keepalived.conf`。

配置 HA-master 的 keepalived：
```
global_defs {
   router_id HA_DEVEL
}

vrrp_instance VI_1 {        #主从实例1
    state MASTER            #HA-master（172.18.216.115）为主，
                            #HA-slave（172.18.216.79）为备
                            #在HA-slave上，该处设置为BACKUP
    interface ens192        #与实际网卡的名称必须保持一致
    virtual_router_id 88    #实例1的VRID为88
    garp_master_delay 1     #在切换到master状态后，延迟进行gratuitous ARP请求
    priority 100            #HA-master的优先级为100，HA-slave的优先级为99
                            #在HA-slave上，该选项设置为99
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }

    virtual_ipaddress {
        172.18.216.194       #实例1的虚拟IP
    }
}
```
接下来再配置 HA-slave 的 keepalived 配置文件。HA-slave 与 HA-master 的配置文件除了`state`项与`priority`项不同以外，其他项完全相同。

配置完成后，在两台虚机上都用`service keepalived start`命令启动 keepalive 服务。之后在 HA-master 上使用`ip addr show`命令可以看到当前节点已经绑定了虚拟 IP。且可以通过关闭 HA-master 上的 keepalive 服务来查看虚拟 IP 是否浮动到了 HA-slave。

> 但目前 haproxy 服务停止时，keepalived 服务并不会停止，所以还需要写一个脚本，使得当 haproxy 服务停止时，keepalived 服务也会停止


### 前端配置 HAProxy

在 HA-master 与 HA-slave 上安装 HAProxy：`yum install haproxy`，然后配置 HAProxy（路径`/etc/haproxy/haproxy.cfg`）。

HAProxy 的配置文件分为五个部分：

- global：全局配置的进程级参数，用来控制 Haproxy 启动前的一些进程及系统设置
- defaults：配置默认参数，可以被 frontend，backend，listen 段继承使用
- frontend：定义接收请求的前端虚拟节点，可根据用户所请求的不同域名、URL 等做不同的请求处理
- backend：定义处理业务的后端服务器集群，以及设置后端的权重、队列、连接数等选项
- listen：frontend 和 backend 的组合体

> 对配置参数的更详细说明请查阅文末的参考文档。

以下是 HA-master 与 HA-slave 上的配置示例：
```
global
    log         127.0.0.1 local2      # 定义日志输出设置
    chroot      /var/lib/haproxy      # chroot运行路径
    pidfile     /var/run/haproxy.pid  # haproxy进程PID文件
    maxconn     20000                  # 默认最大连接数
    daemon                            # 以后台形式运行harpoxy
#---------------------------------------------------------------------
# common defaults that all the 'listen' and 'backend' sections will
# use if not designated in their block
#---------------------------------------------------------------------
defaults
    mode                    http         # 所处理的类别(7层代理http，4层代理tcp)
    log                     global       # 引入global定义的日志格式
    option                  httplog      # 日志类别为http日志格式
    option                  dontlognull  
    option http-server-close    # 当客户端超时时，允许服务器关闭连接
    option forwardfor       except 127.0.0.0/8    # 在响应头部加入forwardfor
    option                  redispatch    # 在使用了基于cookie的会话保持的时候，通常需要
                                          # 加这么一项，一旦后端某一server宕机时，能够将
                                          # 其会话重新派发到其它的servers
    retries                 3             # 3次连接失败就认为服务器不可用
    timeout http-request    10s           
    timeout queue           1m            
    timeout connect         10s           
    timeout client          1m            
    timeout server          1m
    timeout http-keep-alive 10s           # 默认持久连接超时时间
    timeout check           10s           # 心跳检查超时时间
    maxconn                 5000          # 最大并发连接数
#---------------------------------------------------------------------
# main frontend which proxys to the backends
#---------------------------------------------------------------------
frontend  proxy *:80    #前端代理
    default_backend             dynamic
#---------------------------------------------------------------------
# round robin balancing between the various backends
#---------------------------------------------------------------------
backend dynamic    #后端动态服务器
    balance     roundrobin
    cookie      SESSION_ID insert indirect nocache    #设置cookie保持
    server      web1  172.18.218.149:80 inter 3000 rise 2 fall 3 check maxconn 5000 cookie A
    server      web2  172.18.216.107:80 inter 3000 rise 2 fall 3 check maxconn 5000 cookie B
listen statistics  #设置HAProxy 的自带管理系统
        mode http
        bind *:8080    #把stats页面绑定到8080端口
        stats enable   #开启stats功能
        stats auth admin:admin    #认证的用户名和密码
        stats uri /admin?stats    #指定uri访问路径
        stats hide-version        #为了安全（版本bug），隐藏版本信息
        stats refresh 5s          #页面5秒刷新一次
```



# 参考文档

[keepalived+haproxy双主高可用负载均衡](http://nmshuishui.blog.51cto.com/1850554/1405486)
[HAProxy用法详解 全网最详细中文文档](http://www.ttlsa.com/linux/haproxy-study-tutorial/)
[haproxy配置详解](http://leejia.blog.51cto.com/4356849/1421882)
[HAproxy指南之haproxy配置详解](http://blief.blog.51cto.com/6170059/1750952)

