# 配置虚拟云主机(CentOS 7)
以下所有操作均在 root 权限下完成。
## 安装操作系统
以 vSphere Client 为例，当一个新的云虚拟机（非模板复制）选择完硬件配置并创建完成后，需要在该虚拟机上安装操作系统：

 1. 下载操作系统的 ISO 文件（如 CentOS-7-x86_64-DVD-1511.iso ）到本地。
 2. 通过本地的 VMware Workstation ，设置虚拟机的光驱为“启动时连接”与“已连接”，并使用ISO镜像文件为本地已下载的操作系统ISO文件。
 3. 重新启动虚拟机，进入操作系统安装界面，等待一段时间后安装完成。

可通过`passwd`命令来修改root密码；编辑/etc/hostname来修改主机名（重启后生效）。
## 配置IP地址
安装完操作系统后，由于 CentOS7 默认不开启网络，故需要修改一下配置才能使虚拟机自动获得由物理机所分配的IP地址。

1. 使用命令`cd /etc/sysconfig/network-scripts/` ，找到以太网卡配置文件 ifcfg-e\*\* 文件，文件名后面的数字一般是随机生成的。把该文件里onboot的值修改为yes。此外，如果遇到网络服务重启失败，可以查看该文件里的 Mac 地址与`ipconfig`命令所查询到的 Mac 地址是否相同。
2. 若`ifconfig`命令无法使用，则需使用`yum install net-tools.x86_64` 命令来安装该网络工具包。安装完成后使用该命令即可查看虚拟机所获得的IP。

~~若发现无法ping通一些域名，可打开`vi /etc/resolv.conf`，增加条目 nameserver 8.8.8.8 或者 nameserver 114.114.114.114（其他可用的DNS服务器亦可）。~~ 若无法ping通域名，在 ifcfg-e\*\* 文件中设置 DNS1 = 8.8.8.8 或 114.114.114.114。

若需使同一网络上的各个虚机能互相解析彼此的主机名为IP地址，需要在每个虚机的 /etc/hosts 文件里写入每一台虚机的IP地址与主机名。如`172.18.216.211 mon`。具体参考 [/etc/hosts详解](http://os.51cto.com/art/200803/68170.htm) 。

## 更改yum源
Linux的默认官方yum源在国内访问不佳、速度慢，因此把yum源更改为国内比较好的 [阿里云开源镜像站](http://mirrors.aliyun.com/help/centos) 或者 [清华大学开源镜像站](https://mirrors.tuna.tsinghua.edu.cn/help/centos/) 能获得极大的下载速度提升。

在修改完`/etc/yum.repos.d/`下yum源的CentOS-Base.repo后，依次执行`yum clean all`与`yum makecache`来删除与更新yum源的缓存。若在执行命令的过程中发现yum源总是切换到速度满的其他yum源进行下载，则可以在目录下修改该劣质yum源的repo文件，把其enabled值设置为 0 即可。

> 使用`yum install epel-release`命令可安装 epel 源，该源提供了很多扩展性的功能软件。


## 关闭防火墙与SELinux
使用某些网络应用时可能需要关闭防火墙与SELinux服务。

关闭 SELinux：编辑 /etc/selinux/config ，设置SELINUX = disabled； 执行`# setenforce 0`可即时生效。可使用`# getenforce`命令查看SELinux状态。

关闭防火墙服务：

 ```
 # systemctl stop firewalld
 # systemctl disable firewalld
 ```
 
## 更改语言
修改配置文件`/etc/locale.conf`。若改为英文则写入：`LANG="en_US.UTF-8"`，改为中文则写入：`LANG="zh_CN.UTF-8"`。
