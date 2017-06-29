# 配置集群共享文件 NFS 服务器

## 简介

在 Web 服务中往往需要涉及到一些不储存在数据库中的文件资源（比如用户上传的图片、文件等），而在 Web 服务器集群中，若每个服务器节点都有独立的文件资源存储的话，会造成节点间存储不一致的后果。因此比较成熟的解决方案是构建一个 NFS（Network File System）服务器专门提供服务器节点间的共享文件存储。当其他所有 Web 服务器挂载共享目录后，每次读写共享文件资源时实际上读写的是 NFS 服务器上的共享文件系统，这样服务器节点间的存储就可以保持一致性。

## 安装与配置

首先在服务器节点上安装 NFS 服务：`yum install nfs-utils rpcbind`，然后在客户端节点上安装 NFS 服务：`yum install nfs-utils`。

配置 NFS 服务器（配置文件路径`/etc/exports`），配置文件中的每一行表示设置一个共享目录以及其有访问权限的主机地址。以下是一个说明示例：
```
# 共享目录路径为“/home/share”，对所有主机可读，对地址为192.168.1.19的主机可读可写
/home/share *(sync,ro,no_root_squash) 192.168.1.19(sync,rw,no_root_squash)

# 共享目录路径为“/home/pub”，对192.168.152.0子网内的所有主机可读
/home/pub 192.168.152.0/24(sync,ro,no_root_squash)
```

- sync：设置NFS服务器同步写磁盘，这样不会轻易丢失数据，建议所有的NFS共享目录都使用该选项
- ro：设置输出的共享目录只读，与 rw 不能共同使用
- rw：设置输出的共享目录可读写，与 ro 不能共同使用
- root_squash：远程登录 NFS 主机后，使用该共享目录时相当于该目录的拥有者。但是如果是以 root 身份使用这个共享目录的时候，那么这个使用者（root）的权限将被压缩成为匿名使用者，即通常他的 UID 与 GID 都会变成nobody那个身份（较为安全）
- no_root_squash：远程登录 NFS 主机后，使用该共享目录时相当于该目录的拥有者，如果是 root 的话，那么对于这个共享的目录来说，他就具有 root 的权限（不安全）
- all_squash：不论登入 NFS 的使用者身份为何，他的身份都会被压缩成为匿名使用者，通常也就是 nobody

## 启动与挂载
NFS 服务器启动 nfs 服务：`service nfs start`后， NFS 客户端即可进行挂载操作：`mount {{NFS服务器地址}}:{{远程共享目录}} {{本地挂载目录}}`，如`mount 192.168.216.128:/home /mnt`。客户端卸载 NFS 共享时：`umount {{本地挂载目录}}`。

挂载完成，但是这只是临时挂载，客户端重启后 NFS 挂载就失效了，要设置永久挂载可以编辑文件：  
```
vim /etc/fstab 
{{NFS服务器地址}}:{{远程共享目录}} {{本地挂载目录}} nfs defaults 0 0 
```
保存配置，执行mount -a 命令

> PS：客户端不需启动 nfs 服务，但需要安装 nfs 来支持挂载共享目录。客户端卸载共享目录时需保证当前工作目录不是所卸载的目录。

## NFS 的常用命令
showmount 命令：

- showmount -e：显示 NFS 服务器的输出目录列表
- showmount -d：显示当前主机 NFS 服务器中已经被 NFS 客户机挂载使用的共享目录
- showmount -a：显示当前主机中 NFS 服务器的客户机信息
- showmount -a [主机]：显示指定主机中 NFS 服务器的客户机信息

exportfs 命令：

- exportfs -rv：使 NFS 服务器重新读取 exports 文件中的设置
- exportfs -auv：停止当前主机中 NFS 服务器的所有目录输出

## 参考文档
[Linux 系统中文件共享之 NFS](http://www.swanlinux.net/2013/02/12/linux_nfs/)

[NFS 文件共享配置参数](https://www.cnyunwei.cc/archives/148)