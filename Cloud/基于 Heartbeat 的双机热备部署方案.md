# Heartbeat 部署方案（CentOS）

> 注意：Heartbeat 方案本人还未有实践过

## 安装
两种安装方式：

- 主从节点都使用`yum install heartbeat*`命令安装 Heartbeat（须确保已安装 epel 扩展软件包源）。
- 在 Linux-HA 官网下载 [Heartbeat](http://www.linux-ha.org/wiki/Downloads)。

## 配置

Heartbeat 主要的配置文件有 3 个，分别是 **authkeys**，**ha.cf** 和 **haresources**。其中 ha.cf 是主配置文件，haresource 用来配置要让 Heartbeat 托管的服务，authkey 是用来指定 Heartbeat 的认证方式。

> 在 Heartbeat 安装后，默认并没有这三个文件，可以直接从解压的源码目录中找到。

这里以 master/slave 两节点为例，示例的配置文件为 master 节点的。

### 认证文件（/etc/ha.d/authkeys）
该文件为 Heartbeat 的认证文件，该文件主要是用于集群中两个节点的认证，采用的算法和密钥（如果有的话）在集群中节点上必须相同。目前提供了 3 种算法：crc/md5/sha1。其中 crc 不能够提供认证，它只能够用于校验数据包是否损坏，而 sha1/md5 需要一个密钥来进行认证。

```
auth 2
#1 crc
2 sha1 somewords
#3 md5 somewords
```

以上示例中使用的是 sha1 算法，如果要换用其他算法只需要修改 auth 指令后面的数字，然后取消相应行的注释即可。

> 注意：该文件的属性必须为600，否则 Heartbeat 启动将失败。且两个节点的 authkeys 文件内容及权限相同。

### 主配置文件（/etc/ha.d/ha.cf）

该文件是 Heartbeat 的主配置文件。

```
keepalive 2
warntime 5
deadtime 30
initdead 120
udpport 6942
bcast eth0
# mcast eth0 225.0.0.1 694 1 0
ucast eth1 {{ slave的IP地址 }}
auto_failback off
watchdog /dev/watchdog
node host41 host42
# ping 172.16.12.1 ping_group group1 172.16.12.1
respawn hacluster /usr/lib64/heartbeat/ipfail
respawn hacluster /usr/lib64/heartbeat/dopd
apiauth dopd gid=haclient uid=hacluster
use_logd yes
```

- keepalive：发送心跳报文的间隔。默认单位为秒，也可以使用 500ms 来指代 500 毫秒，等同于 0.5。
- warntime：认为对方可能宕掉的间隔时间。
- deadtime：认为对方宕掉的间隔时间，超过这个时间，则认为对方已经宕掉。
- initdead：等待对方启动的最大时间。
- udpport：heartbeat 广播/单播通讯使用的 udp 端口。
- bcast：心跳所使用的网络接口。
- ucast：单播通讯，对方网络接口及IP地址。
- mcast：组播通讯，参数如右：通讯所用的接口 绑定的组播IP（224.0.0.0-239.255.255.255）通讯端口 ttl 是否允许环回。
- auto_failback：表示当主节点（即提供资源/服务的节点）正常之后是否将资源/服务切换回来。
- watchdog：看门狗定时器，如果节点一分钟内没有心跳，则重启节点。
- node：heartbeat 集群中的节点信息（节点的主机名: uname -n）。
- ping/ping_group：用于建立伪集群成员，作用是监测物理链路，如果该节点与伪集群成员不相通，那么该节点无权接管资源/服务。

另一从节点（slave）需要将 ha.cf 文件中 ucast 的 IP 地址改为主节点（master）的 IP 地址。

### 资源文件（/etc/ha.d/haresources）
haresources 文件用于指定双机系统的主节点、集群IP、子网掩码、广播地址以及启动的服务等集群资源。文件每一行可以包含一个或多个资源脚本名，资源之间使用空格隔开，参数之间使用两个冒号隔开。在两个节点上该文件必须完全一致，此文件的一般格式为：
```
node-name network <resource-group>
```
node-name 表示主节点的主机名，必须和 ha.cf 文件中指定的节点名一致；network 用于设定集群的 IP 地址、子网掩码、网络设备标识等（这里指定的IP地址就是集群对外服务的IP地址），resource-group 用来指定需要 Heartbeat 托管的服务，也就是这些服务可以由 Heartbeat 来启动和关闭，如果要托管这些服务，必须将服务写成可以通过 start/stop 来启动和关闭的脚本，然后放到 /etc/init.d/ 或者 /etc/ha.d/resource.d/ 目录下，heartbeat 会根据脚本的名称自动去 /etc/init.d 或者 /etc/ha.d/resource.d/ 目录下找到相应脚本进行启动或关闭操作。

以下是一个具体实例：
```
node1 IPaddr::192.168.60.200/24/eth0/  Filesystem::/dev/sdb5::/webdata::ext3  httpd tomcat
```
其中，node1 是 HA 集群的主节点，IPaddr 为 HeartbeatH自带的一个执行脚本，Heartbeat 首先将执行`/etc/ha.d/resource.d/IPaddr 192.168.60.200/24 start`的操作，也就是虚拟出一个子网掩码为 255.255.255.0，IP为 192.168.60.200 的地址，此IP为 Heartbeat 对外提供服务的网络地址，同时指定此 IP 使用的网络接口为 eth0，接着，Heartbeat 将执行共享磁盘分区的挂载操作，`Filesystem::/dev/sdb5::/webdata::ext3`相当于在命令行下执行 mount 操作，即“mount –t ext3 /dev/sdb5 /webdata”，最后依次启动 httpd 和 tomcat 服务。

> 注意：主节点和从节点中资源文件 haresources 一般要完全一致。

### 参考文档

[Linux-HA开源软件Heartbeat（配置篇）](http://ixdba.blog.51cto.com/2895551/548625)
[heartbeat配置相关](https://github.com/chenzhiwei/linux/tree/master/heartbeat)