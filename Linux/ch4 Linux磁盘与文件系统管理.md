# Linux磁盘与文件系统管理
## 1. EXT2文件系统

Linux 操作系统的文件数据包括文件内容和文件属性，其中权限和属性放置到 inode 中，实际数据放置到 data block 中。每个 inode 与 block 都有编号。

![数据访问示意图](http://cn.linux.vbird.org/linux_basic/0230filesystem_files/filesystem-1.jpg)


### EXT2文件系统的组成部分

![EXT2文件系统的组成部分](http://cn.linux.vbird.org/linux_basic/0230filesystem_files/ext2_filesystem.jpg)

- date block（数据块）
	- 用于放置文件内容，若文件过大则会占用多个block
- inodetable （inode 表）
	- 记录文件属性以及文件的实际内容所放置的 block 编号
	- 每个 inode 大小固定为128 Bytes，每个文件仅会占用一个 inode
	- 系统读取文件时需先读文件的 inode，若其所记录的权限允许，才可实际读取 block 的内容
- superblock（超级块）
	- 记录文件系统的整体信息，包括 inode 与 block 的总量、使用量、剩余量，以及文件系统的格式与相关信息等 
- File system Description（文件系统描述说明）
	- 描述每个 block group 的开始与结束的 block 号码
    - 说明每个区段（包括superblock、bitmap、inodemap、data block）分别介于哪个 block 号码之间
- block bitmap（块对照表）
	- 记录每个 block 的使用情况
- inode bitmap（inode对照表）
    - 记录每个 inode 的使用情况

### 与目录树的关系
当新建一个文件时，该文件被分配一个 inode 以及适应文件大小的多个 block。

当在 Ext2 文件系统中新建一个目录时，该目录被分配一个 inode 以及至少一个 block。其中 inode 记录该目录的相关权限与属性，并记录分配到的 block 的号码；而 block 记录在该目录下的文件名与该文件名占用的 inode 的编号，如下所示：

![目录block](http://cn.linux.vbird.org/linux_basic/0230filesystem_files/dir_block.jpg)

当读取目录树时，系统读取挂载点的信息 从而得到根目录（广义上的）的 inode 内容，并根据该 inode 读取根目录内的文件数据，逐层向下读直到读取正确的文件名。

