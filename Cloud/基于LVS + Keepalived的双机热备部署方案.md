# LVS + keepalived 双机高可用部署方案（CentOS）

### 前期准备
准备四台虚机，分别记作 LVS-master、LVS-slave、web-node1、web-node2。前两者作为 LVS 负载均衡调度器，后两者是提供应用服务的 web 服务器。

安装`epel-realease`源，关闭所有虚机的防火墙与 SELinux，编辑所有节点的`/etc/hosts`文件设置主机名互相解析。使用`yum install ntpdate`安装 ntpdate，并通过`ntpdate 202.120.2.101`命令进行时间同步。

> 202.120.2.101 是上海交通大学网络中心 NTP 服务器的地址


### web 节点配置
在两台 web 机上开启 httpd 服务，并编辑 Real Server （真实服务器，简称 RS）用于绑定 VIP （虚拟 IP）脚本`realserver.sh`如下：

```
#!/bin/bash  
#   
# Script to start LVS DR real server.   
# description: LVS DR real server   
#   
.  /etc/rc.d/init.d/functions
VIP=192.168.18.200   # 在此处设置VIP  
host=`/bin/hostname`
case "$1" in  
start)   
       # Start LVS-DR real server on this machine.   
        /sbin/ifconfig lo down   
        /sbin/ifconfig lo up   
        echo 1 > /proc/sys/net/ipv4/conf/lo/arp_ignore   
        echo 2 > /proc/sys/net/ipv4/conf/lo/arp_announce   
        echo 1 > /proc/sys/net/ipv4/conf/all/arp_ignore   
        echo 2 > /proc/sys/net/ipv4/conf/all/arp_announce
        /sbin/ifconfig lo:0 $VIP broadcast $VIP netmask 255.255.255.255 up  
        /sbin/route add -host $VIP dev lo:0
;;  
stop)
        # Stop LVS-DR real server loopback device(s).  
        /sbin/ifconfig lo:0 down   
        echo 0 > /proc/sys/net/ipv4/conf/lo/arp_ignore   
        echo 0 > /proc/sys/net/ipv4/conf/lo/arp_announce   
        echo 0 > /proc/sys/net/ipv4/conf/all/arp_ignore   
        echo 0 > /proc/sys/net/ipv4/conf/all/arp_announce
;;  
status)
        # Status of LVS-DR real server.  
        islothere=`/sbin/ifconfig lo:0 | grep $VIP`   
        isrothere=`netstat -rn | grep "lo:0" | grep $VIP`   
        if [ ! "$islothere" -o ! "isrothere" ];then   
            # Either the route or the lo:0 device   
            # not found.   
            echo "LVS-DR real server Stopped."   
        else   
            echo "LVS-DR real server Running."   
        fi   
;;   
*)   
            # Invalid entry.   
            echo "$0: Usage: $0 {start|status|stop}"   
            exit 1   
;;   
esac   
```
使用 `chmod +x realserver.sh`命令给脚本文件添加执行权限，并通过`/.realserver.sh start`命令启动该脚本的服务。该服务的作用是使 RS 的网卡与 VIP 进行绑定，从而可允许 RS 处理来自负载调度器转发的请求（DR 模式）。启动该服务后可用`ifconfig`命令查看是否已绑定 VIP。

### LVS 节点配置
LVS 节点使用`yum install keepalived ipvsadm`命令安装 keepalived 服务与 LVS 服务。

配置文件的路径是`/etc/keepalived/keepalived.conf`。keepalived 配置文件以 block 形式组织，每个块内容都包含在`{}`中。keepalived 配置分为三类：

- 全局配置：对整个 keepalived 都生效的配置
- VRRPD 配置：核心配置，主要实现高可用功能
- LVS 配置：LVS 相关功能的配置

```
######################
#  全局配置（大部分选项为邮件通知服务的参数。可设置为空）
######################
global_defs {                               # global_defs 全局配置标识 
                                            --------------------------------------
   notification_email {                     # notification_email用于设置报警邮件地址
     acassen@firewall.loc                   # 可以设置多个，每行一个
     failover@firewall.loc                  # 设置邮件报警，需开启本机Sendmail 服务
     sysadmin@firewall.loc                  # yum -y install mailx sendmail
   }                                        --------------------------------------
   
   notification_email_from 233@qq.com  # 设置邮件发送地址
   smtp_server 192.168.200.1           # 设置邮件的smtp server地址
   smtp_connect_timeout 30             # 设置连接smtp sever超时时间
   router_id LVS_DEVEL                 # 表示运行keepalived服务器标识
									   # 发邮件时会显示在邮件主题中
}

######################
#  VRRPD配置
######################

vrrp_instance VI_1 {         # VRRPD 配置标识 VI_1是实例名称

    state MASTER             # 指定Keepalvied角色。
                             # MASTER表示此主机为主服务器，BACKUP则是表示为备用服务器
    interface eth0           # 指定HA监测网络的接口。检查是否与ifconfig命令查看的网卡名称一致。
    virtual_router_id 51     # 虚拟路由标识，标识为数字，同一个VRRP实例使用唯一的标识
                             # 即可表示在同一个vrrp_instance下 MASTER_ID = BACKUP_ID
    priority 100             # 定义节点优先级，数字越大表示节点的优先级越高
                             # 同一个VRRP_instance下
                             # 必须 MASTE_PRIORITY > BACKUP_PRIORITY 
    advert_int 1             # 设定MASTER与BACKUP主机质检同步检查的时间间隔，单位为秒
             
    authentication {         # 设定节点间通信验证类型和密码，验证类型主要有PASS和AH两种
        auth_type PASS       # 同一个vrrp_instance，MASTER验证密码和BACKUP保持一致
        auth_pass 1111
    }
    
    virtual_ipaddress {      # 设置虚拟IP地址 (VIP)，也可仅设置一个
        192.168.200.16
        192.168.200.17
        192.168.200.18
    }
}

######################
# LVS配置
######################

virtual_server 192.168.18.200 80 {    # virtual_server LVS配置标识 
                                      # 格式：virtual_server [VIP] [port]
    delay_loop 6     # 设置健康检查时间间隔，单位为秒   
    lb_algo rr       # 设置负载调度算法，可用的调度算法有：rr、wlc、lc、lblc、sh、dh等
    lb_kind DR       # 设置LVS实现负载均衡的机制，有NAT、TUN和DR三种模式可选                   
    nat_mask 255.255.255.0   # NAT子网掩码
    persistence_timeout 50  # 会话保持时间 
    protocol TCP             # 指定转发协议类型
    
#---------------------------------------------------------------------------------
# persistence_timeout 会话保持时间对动态网页非常有用，为集群系统中的seesion共享提供了一个很好的解决方案
# 用户的请求会一直分发到某个服务节点，直至超过这个会话的保持时间（指最大无响应超时时间）
# =[用户操作动态页面如果在50s没有执行任何操作则被分发到另外的节点]
#---------------------------------------------------------------------------------

    real_server 192.168.18.201 80 { # 设置real server段开始的标识 [IP为真实IP地址]
        weight 1                    # 用于配置real server节点的权值，数字越大，权值越高
                                    # 设置权值大小可以为不同性能的服务器分配不同的负载
        HTTP_GET {   
            url {   
              path /   
          status_code 200   
            }   
            connect_timeout 2   
            nb_get_retry 3   
            delay_before_retry 1   
        }   
    }   
    real_server 192.168.18.202 80 {   
        weight 1   
        HTTP_GET {   
            url {   
              path /   
              status_code 200   
            }   
            connect_timeout 2   
            nb_get_retry 3   
            delay_before_retry 1   
        }   
    }   
}
```

keepalived 的配置文件路径在`/etc/keepalived/keepalived.conf`。LVS-master 与 LVS-slave 的配置文件除了 VRRPD 配置中的状态与优先级这两个参数不同外，其他参数应当相同。

配置完成后，启动 LVS-master 与 LVS-slave的 keepalived 服务：`service keepalived start`，并可使用`ipvsadm -L -n`命令查看 LVS 状态。

> Tips：可使用`service keepalived status`命令查看 keepalived 服务的 log。

### 测试

通过关闭与开启 LVS-master 的 keepalived 服务，观察 VIP 在 LVS 节点上的浮动情况。通过关闭与开启某一个 web 节点的 web 服务，观察集群的高可用是否生效。

### 参考文档
实验步骤参考：[Linux 高可用集群之keepalived详解](http://freeloda.blog.51cto.com/2033581/1280962)
详细配置参数参考：[Keepalived 工作原理及简要安装](https://my.oschina.net/luciamoore/blog/607034)