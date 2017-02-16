# Linux的文件权限与目录配置
## 用户与用户组
Linux的每个文件中，依据权限分为用户、用户组与其他人三种身份。用户可以有多个用户组的支持。

- 默认情况下，系统上所有用户账号的相关信息都储存在 /etc/passwd 文件中。
- 个人密码存储在 /etc/shadow 文件中
- 所有组名都存储在 /etc/group 文件中

## Linux文件权限概念

### Linux文件属性
使用命令`# ls -al`可查看当前目录下所有文件的详细权限与属性，如：
```
[root@www ~]# ls -al
total 156
drwxr-x---   4    root   root     4096   Sep  8 14:06 .
drwxr-xr-x  23    root   root     4096   Sep  8 14:21 ..
-rw-------   1    root   root     1474   Sep  4 18:27 anaconda-ks.cfg
-rw-------   1    root   root      199   Sep  8 17:14 .bash_history
-rw-r--r--   1    root   root       24   Jan  6  2007 .bash_logout
-rw-r--r--   1    root   root      191   Jan  6  2007 .bash_profile
-rw-r--r--   1    root   root      176   Jan  6  2007 .bashrc
-rw-r--r--   1    root   root      100   Jan  6  2007 .cshrc
drwx------   3    root   root     4096   Sep  5 10:37 .gconf      <=范例说明处
drwx------   2    root   root     4096   Sep  5 14:09 .gconfd
-rw-r--r--   1    root   root    42304   Sep  4 18:26 install.log <=范例说明处
-rw-r--r--   1    root   root     5661   Sep  4 18:25 install.log.syslog
[    1   ][  2 ][   3  ][  4 ][    5   ][     6     ][       7          ]
[  权限  ][连结][拥有者][群组][文件容量][  修改日期 ][      文件名        ]
```

文件属性示意图如下：

![enter image description here](http://cn.linux.vbird.org/linux_basic/0210filepermission_files/0210filepermission_2.gif)

第一列代表该文件的类型与权限，共计有十个字符：

- 第一个字符代表该文件的类型：
	- [d] 表示目录
	- [-] 表示文件
	- [|] 表示链接文件
- 接下来的字符以3个为一组，且均为 “rwx” 的3个参数的组合。“rwx” 分别代表可读、可写与可执行。三个权限的位置不会改变，**若没有权限则会出现\[\-\]**。
	- 第一组为“文件所有者”的权限。
	- 第二组为“同用户组”的权限。
	- 第三组为“其他非本用户组的权限”。

![enter image description here](http://cn.linux.vbird.org/linux_basic/0210filepermission_files/0210filepermission_3.gif)

第二列表示有多少文件名链接到此节点（i-node）：

- 每个文件会将它的权限与属性记录到文件系统的 i-node 中，由于目录树是使用文件名来记录，因此每个文件名就会链接到一个 i-node 。
- 该属性记录有多少不同的文件名链接到同一个 i-node 。

第三列表示该文件（或目录）的所有者用户。

第四列表示该文件的所属用户组。

第五列表示该文件的容量大小，默认单位为 Byte 。

第六列表示该文件的创建文件日期或是最近的修改日期。

第七列表示该文件的文件名，但如果文件名前多一个“ . ”，则表示该文件为“隐藏文件”。

### 改变文件属性与权限
在复制文件给其他用户等情况下，需要改变文件的所有者或者权限。

#### 改变文件所属用户组：chgrp
```
#语法：
[root@www ~]# chgrp [-R] 用户组名称 文件或目录名

#-R : 进行递归(recursive)的持续变更，亦即连同次目录下的所有文件、目录都更新成为这个群组之意。
     
#范例：改变文件install.log的用户组为users
[root@www ~]# chgrp users install.log
```

#### 改变文件所有者：chown
```
#语法：
[root@www ~]# chown [-R] 账号名称 文件或目录
[root@www ~]# chown [-R] 账号名称:组名 文件或目录

#-R : 进行递归(recursive)的持续变更，亦即连同次目录下的所有文件都变更

#范例：将install.log的拥有者改为bin这个log用户：
[root@www ~]# chown bin install.log

#范例：将install.log的拥有者与群组改回为root：
[root@www ~]# chown root:root install.log
```

#### 改变文件权限：chmod
有两种权限设置方法：数字类型更改权限与符号类型更改权限。

- 数字类型更改权限
	- 使用数字来代表“rwx”三个权限，其中 r：4；w：2；x：1。
	- 每种身份（owner，group，others）各自的三个权限数字需要累加。
	- 如当权限为 [-rwxrwx---] 时，分数则是：owner = rwx = 7 ；group = rwx = 7 ；others = --- =0 。因此总的权限分数就是 770 。
	- 更改权限的命令语法：`# chmod [-R] xyz 文件或目录`，xyz 即为总的权限分数。
- 符号类型改变文件权限
	- 用 u、g、o 分别代表 user、group、others 3种身份，此外 a 代表 all，即全部的身份。读写的权限可以写成 r，w，x 。可使用的操作符号有 +（加入）、- （除去）、= （设置）。
	- 更改权限的命令语法：`# chmod [-R] 操作表达式 文件或目录`，操作表达式是如`u=rwx,go=rx`或者`a+w,o-x`的式子。

### 目录与文件的权限意义

#### 文件的权限
- r(read)：读取该文件的内容
- w(write)：编辑该文件的内容但**不可删除该文件**
- x(execute)：该文件具有可被系统执行的权限。一个文件能否被执行与文件名没有绝对关系

#### 目录的权限
- r(read)：读取该目录结构列表的权限
- w(write)：读取该目录结构列表的权限，包括新建、删除、重命名该目录下的文件与目录
- x(execute)：用户能否进入该目录成为工作目录的权限
- 开放目录给人浏览时，至少应给予 r 与 x 的权限，但 w 权限不可随便给予。

## Linux目录配置
FHS（Filesystem Hierarchy Standard）的主要目的在于规范每个特定目录下放置什么样的数据。所定义的三层主目录为/、/var、/usr 。有五个目录不可与根目录放在不同的分区，分别为/etc, /bin, /lib, /dev, /sbin。

![enter image description here](http://cn.linux.vbird.org/linux_basic/0210filepermission_files/directory_tree.gif)
