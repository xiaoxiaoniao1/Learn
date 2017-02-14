# 安装VMware Tools（可选）
VMware Tools 是 VMware 虚拟机中自带的一种增强工具，可实现主机与虚拟机之间的拖拽共享文件，以及鼠标在虚拟机和主机之间自由移动（无须再按 ctrl+alt ）。

在安装完成后，vSphere Client 界面可显示当前虚拟机的IP地址。

安装步骤如下：

1. 在 VMware Workstation 的文件夹下找到 linux.iso 文件，该文件是对应该 VMware Workstation 版本的 VMware Tools 的安装文件。
2. 设置虚拟机光驱的镜像文件为该 linux.iso 文件。
3. 新建一个用于挂载光驱的目录 `mkdir /mnt/cdrom` ，并挂载光驱`mount /dev/cdrom /mnt/cdrom` ，之后便可以从`/mnt/cdrom` 目录中访问光驱里的文件了。
4. 使用 `cd /mnt/cdrom` 进入光驱，输入ls命令查看到有个*.tar.gz格式的文件（如vmware-linux-tools.tar.gz），输入命令`cp vmware-linux-tools.tar.gz /home/`将它复制到/home/目录后，使用`tar -zxf vmware-linux-tools.tar.gz`对其进行解压。
5. 进入解压后的目录，输入命令`./vmware-install.pl` 即可进行安装。若无法识别pl文件，则需`yun install perl` 命令安装perl。
