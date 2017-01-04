# 配置虚拟云主机(CentOS)
以下所有操作均在 root 权限下完成。
## 安装操作系统
以 vSphere Client 为例，当一个新的云虚拟机（非模板复制）选择完硬件配置并创建完成后，需要在该虚拟机上安装操作系统：

 1. 下载操作系统的ISO文件（如CentOS-7-x86_64-DVD-1511.iso）到本地。
 2.  通过本地的 VMware Workstation ，设置虚拟机的光驱为“启动时连接”与“已连接”，并使用ISO镜像文件为本地已下载的操作系统ISO文件。
 3. 重新启动虚拟机，进入操作系统安装界面，等待一段时间后安装完成。

## 配置IP地址
安装完操作系统后，虚拟机并不能直接连接到网络，需要修改一下配置才能使虚拟机自动获得由物理机所分配的IP地址。

1. 使用命令`cd /etc/sysconfig/network-scripts/` ，找到以太网卡配置文件ifcfg-enp**文件，文件名后面的数字一般是随机生成的。把该文件里onboot的值修改为yes。
2. 若`ifconfig`命令无法使用，则需使用`yum install net-tools.x86_64` 命令来安装该网络工具包。安装完成后使用该命令即可查看虚拟机所获得的IP。

## 安装VMware Tools（可选）
VMware Tools 是 VMware 虚拟机中自带的一种增强工具，可实现主机与虚拟机之间的拖拽共享文件，以及鼠标在虚拟机和主机之间自由移动（无须再按 ctrl+alt ）。

此外，在安装完成后 vSphere Client 界面可显示当前虚拟机的IP地址。

安装步骤如下：

1. 在 VMware Workstation 的文件夹下找到 linux.iso 文件，该文件是对应该 VMware Workstation 版本的 VMware Tools 的安装文件。
2. 设置虚拟机光驱的镜像文件为该 linux.iso 文件。
3. 新建一个用于挂载光驱的目录 `mkdir /mnt/cdrom` ，并挂载光驱`mount /dev/cdrom /mnt/cdrom` ，之后便可以从`/mnt/cdrom` 目录中访问光驱里的文件了。
4. 使用 `cd /mnt/cdrom` 进入光驱，输入ls命令查看到有个*.tar.gz格式的文件（如vmware-linux-tools.tar.gz），输入命令`cp vmware-linux-tools.tar.gz /home/`将它复制到/home/目录后，使用`tar -zxf vmware-linux-tools.tar.gz`对其进行解压。
5. 进入解压后的目录，输入命令`./vmware-install.pl` 即可进行安装。若无法识别pl文件，则需`yun install perl` 命令安装perl。


