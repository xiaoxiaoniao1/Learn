
Lysncd 实际上是 lua 语言封装了 inotify 和 rsync 工具，采用了 Linux 内核（2.6.13 及以后）里的 inotify 触发机制，然后通过 rsync 去差异同步，达到实时的效果。它完美解决了 inotify + rsync 海量文件同步带来的文件频繁发送文件列表的问题 —— 通过时间延迟或累计触发事件次数实现。

另外，它的配置方式很简单，lua 本身就是一种配置语言，可读性非常强。lsyncd 也有多种工作模式可以选择（本地目录 cp，本地目录 rsync，远程目录 rsyncssh）。

## 安装

### Ubuntu 环境
已经收录在 ubuntu 的官方镜像源里，直接通过`apt-get install lsyncd`命令安装。

### CentOS 环境

安装了 epel-release 扩展源后，通过`yum install lsyncd`命令安装。

## 配置

lsyncd 安装完后默认并没有提供配置文件，因此需要我们自行创建。配置文件 lsyncd.conf 的一个示例如下：

```
# cd /usr/local/lsyncd-2.1.5
# mkdir etc var
# vi etc/lsyncd.conf

settings {
    logfile = "/home/ubuntu/Desktop/lsyncd.log",
    statusFile = "/home/ubuntu/Desktop/lsyncd.status"
}

sync {
    default.rsyncssh,
    source = "/home/ubuntu/Desktop/src",
    host = "192.168.10.133",
    targetdir = "/home/ubuntu/Desktop/dst",
    delay = 15
}
```
### 配置选项说明

**settings**里是全局设置，`--`开头表示注释，下面是几个常用选项说明：

- `logfile` ：设置日志文件
- `stausFile` ：设置状态文件
- `statusInterval` ：将 lsyncd 的状态写入上面的statusFile的间隔，默认10秒
- `inotifyMode` ：指定inotify监控的事件，默认是`CloseWrite`，还可以是`Modify`或`CloseWrite or Modify`
- `maxProcesses` ：同步进程的最大个数。假如同时有20个文件需要同步，而`maxProcesses = 8`，则最大能看到有8个rysnc进程
- `maxDelays` ：累计到多少所监控的事件激活一次同步，即使后面的`delay`延迟时间还未到

**sync**里是定义同步参数。

一般第一个参数指定 lsyncd serv以什么模式运行：**rsync**、**rsyncssh**、**direct** 三种模式：

- `default.rsync` ：**本地目录间同步**。使用 rsync 也可以达到使用 ssh 形式的远程 rsync 效果
`default.direct` ：**本地目录间同步**，使用 cp、rm 等命令完成差异文件备份
`default.rsyncssh` ：**同步到远程主机目录**，rsync 的 ssh 模式，需要使用 key 来认证
- `source` ：同步的源目录，使用绝对路径。
- `target ` ：同步的目的目录，在不同模式下有不同的写法。
- `init` ：当`init=false`时表示跳过初始同步，启动时即使原目录有差异时也不会同步。默认值为`true`。
- `delay` ：等待同步的延时，默认15s，即每15s同步一次。
- `excludeFrom`： 排除选项，后面指定排除的列表文件.

更多参数设置可以在参考文档中查看。

### 启动 lsyncd

使用命令加载配置文件启动：

```
lsyncd -log Exec [CONFIG-FILE]
```

[CONFIG-FILE]为配置文件所在路径。

> 更加详细的说明可以通过`lsyncd -help`查看。

## SSH 密钥配置

为了让`lysncd`能够以 rsyncssh 模式进行工作，我们还需要对备份服务器进行一些配置。

> 主服务器是指需要被备份的服务器，备份服务器是指用来实现主服务器备份的服务器。

### 备份服务器操作

在备份服务器中创建一个密钥对，直接回车即可，然后设置为`authorized_keys`。

```shell
ssh-keygen -t rsa
cd ~/.ssh
cat id_rsa.pub >> authorized_keys
```
然后检查备份服务器有没有安装`openssh-server`，没有的话需要安装。

### 主服务器操作

将备份服务器中生成的私钥`id_rsa`拷贝到主服务器的`~/.ssh/`里面。然后设置好权限，并且测试是否能够正常登陆。

```shell
chmod 600 ~/.ssh/id_rsa
ssh [USER]@[REMOTE_IP]
```

[USER]和[REMOTE_IP]为登陆的用户和备份服务器的IP。如果能成功登陆的话则表示配置成功。

> 也可以在主服务器中生成一对密钥，把公钥拷贝到备份服务器的`~/.ssh/authorized_keys`中。

## 配置文件模式示例

下面的内容几乎涵盖了所有同步的模式。
```
settings {
    logfile ="/usr/local/lsyncd-2.1.5/var/lsyncd.log",
    statusFile ="/usr/local/lsyncd-2.1.5/var/lsyncd.status",
    inotifyMode = "CloseWrite",
    maxProcesses = 8,
    }


-- I. 本地目录同步，direct：cp/rm/mv。 适用：500+万文件，变动不大
sync {
    default.direct,
    source    = "/tmp/src",
    target    = "/tmp/dest",
    delay = 1
    maxProcesses = 1
    }

-- II. 本地目录同步，rsync模式：rsync
sync {
    default.rsync,
    source    = "/tmp/src",
    target    = "/tmp/dest1",
    excludeFrom = "/etc/rsyncd.d/rsync_exclude.lst",
    rsync     = {
        binary = "/usr/bin/rsync",
        archive = true,
        compress = true,
        bwlimit   = 2000
        } 
    }

-- III. 远程目录同步，rsync模式 + rsyncd daemon
sync {
    default.rsync,
    source    = "/tmp/src",
    target    = "syncuser@172.29.88.223::module1",
    delete="running",
    exclude = { ".*", ".tmp" },
    delay = 30,
    init = false,
    rsync     = {
        binary = "/usr/bin/rsync",
        archive = true,
        compress = true,
        verbose   = true,
        password_file = "/etc/rsyncd.d/rsync.pwd",
        _extra    = {"--bwlimit=200"}
        }
    }

-- IV. 远程目录同步，rsync模式 + ssh shell
sync {
    default.rsync,
    source    = "/tmp/src",
    target    = "172.29.88.223:/tmp/dest",
    -- target    = "root@172.29.88.223:/remote/dest",
    -- 上面target，注意如果是普通用户，必须拥有写权限
    maxDelays = 5,
    delay = 30,
    -- init = true,
    rsync     = {
        binary = "/usr/bin/rsync",
        archive = true,
        compress = true,
        bwlimit   = 2000
        -- rsh = "/usr/bin/ssh -p 22 -o StrictHostKeyChecking=no"
        -- 如果要指定其它端口，请用上面的rsh
        }
    }

-- V. 远程目录同步，rsync模式 + rsyncssh，效果与上面相同
sync {
    default.rsyncssh,
    source    = "/tmp/src2",
    host      = "172.29.88.223",
    targetdir = "/remote/dir",
    excludeFrom = "/etc/rsyncd.d/rsync_exclude.lst",
    -- maxDelays = 5,
    delay = 0,
    -- init = false,
    rsync    = {
        binary = "/usr/bin/rsync",
        archive = true,
        compress = true,
        verbose   = true,
        _extra = {"--bwlimit=2000"},
        },
    ssh      = {
        port  =  1234
        }
    }
```

## 参考文档

[Config Layer 4: Default Config](https://axkibe.github.io/lsyncd/manual/config/layer4/)

[Lsyncd | 使用lsyncd同步文件目录](http://clavinli.github.io/2013/11/12/linux-server-lsyncd/)    

[lsyncd实时同步搭建指南——取代rsync+inotify](http://seanlook.com/2015/05/06/lsyncd-synchronize-realtime/)
