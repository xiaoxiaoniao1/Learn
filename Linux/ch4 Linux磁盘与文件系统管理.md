# Linux磁盘与文件系统管理
## 1. EXT2文件系统

Linux 操作系统的文件数据包括文件内容和文件属性，其中权限和属性放置到 inode 中，实际数据放置到 data block 中。每个 inode 与 block 都有编号。

![数据访问示意图](http://cn.linux.vbird.org/linux_basic/0230filesystem_files/filesystem-1.jpg)


### EXT2文件系统的组成部分

EXT2 文件系统在格式化时被区分为多个块组（Block Group），每个块组有独立的 inode/block/superblock 系统。

![EXT2文件系统的组成部分](http://cn.linux.vbird.org/linux_basic/0230filesystem_files/ext2_filesystem.jpg)

- date block（数据块）
	- 用于放置文件内容，若文件过大则会占用多个block
- inode table （inode 表）
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

当读取目录树时，系统读取挂载点的信息从而得到根目录（广义上的）的 inode 内容，并根据该 inode 读取根目录内的文件数据，逐层向下读直到读取正确的文件名。

关于挂载：挂载是文件系统和目录树的结合；挂载点一定是目录，该目录为进入该文件系统的入口。


## 2. 文件系统的简单操作

### 磁盘与目录的容量：df、du
df 用于列出文件系统整体磁盘使用量
```
[root@www ~]# df [-ahikHTm] 目录或文件名
# -h：以GB、MB、KB等格式自行显示
# -i：不用硬盘容量，而以 inode 的数量来显示
```
du用于评估文件系统的磁盘使用量
```
[root@www ~]# du [-ahskm] 目录或文件名
# -h：以易读方式显示
# -s：只列出总量
```

### 连接文件

#### 硬连接或实际连接（hard link）
由于每个文件只会占用一个 inode，文件内容由 inode 的所指向的 block 来指定，且若要读取文件，必须经过目录记录的文件名来指向正确的 inode 。因此**文件名只和目录有关，而文件内容只和 inode 有关**。

此种情况下，则可能有多个文件名对应到同一个 inode 。即：hard link 只是在某个目录下新建一条文件名连接到已有的某 inode 的关联记录而已。

![硬连接的文件读取](http://cn.linux.vbird.org/linux_basic/0230filesystem_files/hard_link1.gif)

上图示意：可通过1或2的目录 inode 指定的 block 找到两个不同的文件名，而不管通过哪个文件名均可以指向 real 这个 inode 来读取最终数据。

hard link 的限制：
1. 不能跨文件系统
2. 不能硬连接到目录（因为硬连接到目录时，连接数据需要连同被连接目录下的所有数据都建立连接，会造成大的复杂度）*#这里不太懂*

#### 符号连接（symbolic link）
符号连接即是创建一个**独立**（即拥有和源文件不一样的 inode）文件，该文件会让数据的读取指向其连接的那个文件的文件名，类似于“快捷方式”。

![符号连接的文件读取](http://cn.linux.vbird.org/linux_basic/0230filesystem_files/symbolic_link1.gif)

上图示意：由1号 inode读取到连接文件的内容仅有文件名，根据文件名连接到正确的目录去取得目标文件的 inode，即可读取到正确数据。

```
[root@www ~]# ln [-sf] 源文件 目标文件
# -s：如果不加任何参数，则是hard link，至于-s则是symbolic link
# -f：目标文件存在时，删除目标文件再创建
```

## 3. 磁盘的分区、格式化、检验和挂载

磁盘管理是对 Linux 系统管理中的重要一环。当想要在系统中新增一块硬盘时，应该：

1. 对磁盘进行分区，以新建可用的分区
2. 对该分区进行格式化，以创建系统可用的文件系统
3. 对新建文件系统进行检验
4. 在 Linux 系统上创建挂载点（也即目录），并将其挂载

以下是几个常用的命令：

- 磁盘分区：fdisk、parted
- 磁盘格式化：mkfs
- 磁盘检验：fsck、badblocks
- 磁盘挂载与卸载：mount、umount

略。

## 4. 设置开机挂载

手动处理 mount 很麻烦，需要设置成让系统在开机时自动挂载。

略。

## 5. 内存交换空间（swap）的构建

swap 的功能是在物理内存不足时作为内存扩展（虚拟内存）。

### 使用物理分区构建 swap
1. 分区：使用 fdisk 在磁盘中分出一个分区给系统作为 swap。
2. 格式化：`mkswap 设备文件名`即可格式化该分区。
3. 使用：`swapon 设备文件名`启动该 swap 设备。
4. 查看：通过`free`查看内存使用情况。

### 使用文件构建 swap
1. 使用`dd`新增一个大文件（如128MB）在 /tmp 下
2. 使用`mkswap`将 /tmp/swap 这个文件格式化为 swap 的文件格式
3. 使用`mkswap`将 /tmp/swap 启动
4. 使用`swapoff`将 /tmp/swap 关闭

