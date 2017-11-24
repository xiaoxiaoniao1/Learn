# Linux服务器部署
## 初始化服务器
首先需安装 Linux 操作系统并对其进行初始化配置。具体步骤请参见该文章：[配置虚拟云主机(CentOS 7)](https://github.com/Zouzhp3/Learn/blob/master/Cloud/%E9%85%8D%E7%BD%AE%E8%99%9A%E6%8B%9F%E4%BA%91%E4%B8%BB%E6%9C%BA%28CentOS%29.md)
 
此外，最好不要用 root 账户直接进行操作，应当设置一个拥有 sudo 权限的新用户，使用该用户进行服务器的操作。

[教程：添加一个新用户并授权](http://www.cnblogs.com/woshimrf/p/5906084.html)
 
## 安装MySQL
在 CentOS 7和 CentOS 7.1系统中，默认安装的 mysql 是它的分支 mariadb ，因此需要从 mysql 的官网中下载。

1. 下载 Yum Repo：
从 [mysql官方下载地址](http://dev.mysql.com/downloads/repo/yum/) 获取 Yum Repo，并使用`yum install`命令进行安装该 Repo：`# yum -y install mysql57-community-release-el7-7.noarch.rpm`。完成后可以用`# yum list | grep mysql`来查看可安装的 mysql 包。
2. 安装 MySQL 数据库的服务器版本：
`# yum install mysql-community-server`
3. 启动服务：
`# service mysqld start`，并可用`# service mysqld status`查看服务状态。
4. 获取初始密码：
使用YUM安装并启动MySQL服务后，MySQL进程会自动在进程日志中打印 root 用户的初始密码。使用`grep "password" /var/log/mysqld.log`可查看日志中的MySQL root 密码。
5. 修改root用户密码：
使用`# mysql -uroot -p`并输入密码后进入 mysql 终端，再使用`mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'new password';`命令修改 mysql 的密码。


注意：如果装的 mysql 版本是5.7，则可能出现修改密码时报错`ERROR 1819 (HY000): Your password does not satisfy the current policy requirements`，这是因为新密码安全性较低。可使用`mysql> set global validate_password_policy=0;`降低密码安全等级后解决。

mariadb 是 mysql 的一个分支版本，与 mysql 不能同时安装，但是接口与 mysql 完全兼容。当数据库需要迁移到 mariadb 时，可能会出现`ImportError: libmysqlclient.so.18`的错误，解决方法为'pip install mysql-client'（这里很奇怪，如果是 mysql 数据库的话不用安装 mysql-client 也可以）。

### 导出数据库（sql脚本）   

`mysqldump -u 用户名 -p 数据库名 > 导出的文件名`

例如：`mysqldump -u root -p db_name > test_db.sql`

### 导入数据库（sql脚本）   

使用`mysql -u root -p`命令进入 MySQL 后：
```
mysql> use test;
mysql> source c:/test.sql
```

### 参考文章
[CentOS 7.2使用yum安装MYSQL 5.7.10](https://typecodes.com/linux/yuminstallmysql5710.html)

[阿里云CentOS 7.1使用yum安装MySql 5.6.24](https://typecodes.com/web/centos7yuminstallmysql5.html)

[修改MySQL 5.7.9版本的root密码方法以及一些新变化整理](http://bbs.bestsdk.com/detail/762.html) 

### 在 CentOS 上安装 mysql-python
在 CentOS 下用`pip install mysql-python`命令直接安装时会出现找不到`mysql_config`、`gcc`等错误，解决方案是安装mysql(或mariadb)的devel包(如mysql-devel或mariadb-devel)，以及安装python的devel包。

## 设置远程访问 MySQL 
linux 上的 mysql 数据库都是默认仅允许本地访问。设置 mysql 为远程访问，可以供开发者在本地使用数据库可视化工具远程连接而不用通过 ssh。

在shell中，$mysql -r -u root -p 输入密码后进入 mysql 数据库。

```
mysql>use mysql;
mysql>update user set host = '%' where user = 'root';    //这个命令执行错误时可略过
mysql>flush privileges;
mysql>select host, user from user; //检查‘%’ 是否插入到数据库中
```

找到文件/etc/mysql/my.cnf 修改 bind-address = 0.0.0.0 之后，重启 mysql 进程：`$service mysqld restart`。

## 安装 virtualenv
首先需安装 python-pip ，若提示没有包可安装，则使用命令`# yum -y install epel-release`安装扩展仓库后再使用 yum 进行安装。使用 pip 安装 virtualenv：`# pip install virtualenv`。

使用virtualenv命令创建python虚拟环境：`# virtualenv [虚拟环境名称]`，之后在本地会生成一个与虚拟环境同名的文件夹。默认情况下虚拟环境不会依赖系统环境的global site-packages，如果想依赖系统环境的第三方软件包，也可以使用参数--system-site-packages。

进入虚拟环境目录，启动虚拟环境，如下：
```
[root@localhost ~]# cd env1/
[root@localhost env1]# source bin/activate
(env1)[root@localhost env1]# python -V
Python 2.7.8
```

部署服务时，可直接把开发者 windows 本地的虚拟环境下的 /Lib/site-packages 复制到 Linux 系统里的虚拟环境中，有些出于 python 版本不同导致的兼容问题可通过重新下载库来解决。


### 参考文章
[使用 virtualenv 搭建独立的 Python 环境](http://qicheng0211.blog.51cto.com/3958621/1561685)

## 开放端口
如果系统的防火墙开启，则需要设置防火墙开放端口。若没有启动防火墙服务，则默认开放所有端口。

当使用脚本启动 flask 服务时可以指定 Host 和 端口：`# python manage.py runserver -h 0.0.0.0 -p 80`（使用80端口时需要 root 权限）

## 使用 supervisor 维护服务进程

supervisor 是用 Python 开发的一套通用的 Linux 进程管理程序，能将一个普通的命令行进程变为后台 daemon，并监控进程状态，使其异常退出时能自动重启。

首先使用`# yum install supervisor`命令安装 supervisor 。查看配置文件`/etc/supervisord.conf`，检查项 [include] 里的应用配置文件应放置在哪个目录，然后在指定目录下新建应用配置文件：
```
[program:app]                                         # app 为具体用户名
command=python manage.py runserver -h 0.0.0.0 -p 5000 # 启动命令，与手动启动命令一样
directory=/home/netlab301/lancs                       # 程序的启动目录
user=root                                             # 启动命令所使用的用户身份
```

启动 supervisor 即可：`supervisord -c /etc/supervisord.conf`

常用命令：
```
ps -aux | grep python  # 查看进程
ps -aux | grep 5000    # 查看占用某端口的进程

supervisorctl status         # 监控状态
supervisorctl stop app       # 停止 app
supervisorctl start app      # 启动 app （往往需要先启动 virtualenv 虚拟环境）
supervisorctl restart app    # 重启 app
```

由于 supervisor 往往需要与虚拟环境同时使用，因此 supervisor 脚本中的 python 命令可以用虚拟环境中的 python 命令替代（如：`/home/ehpcadmin/venv/bin/python manage.py runserver`）

## 使用 gunicorn 作为 Web 服务器

由于 Flask 自带的服务器（通过`runserver`命令启动）性能差且无法支持并发请求，因此需要使用 gunicorn 作为服务器（或其他 web 服务器）来提供更好的性能。

```
Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX. It's a pre-fork worker model. The Gunicorn server is broadly compatible with various web frameworks, simply implemented, light on server resources, and fairly speedy.
```

安装 gunicorn：` pip install gunicorn`

启动 gunicorn 服务器：`gunicron -w4 -b0.0.0.0:8000 myapp:app`，其中 -w 表示开启多少个 worker，-b 表示 gunicorn 开放的访问地址。想要结束 gunicorn 只需执行`pkill gunicorn`。

[Gunicorn 官方文档](http://docs.gunicorn.org/en/stable/run.html)

### gevent
gevent 是第三方库，可通过 greenlet 实现协程，其基本思想是：当一个 greenlet 遇到 IO 操作时，比如访问网络，就自动切换到其他的 greenlet，等到 IO 操作完成，再在适当的时候切换回来继续执行。由于 IO 操作非常耗时，经常使程序处于等待状态，有了 gevent 为我们自动切换协程，就保证总有 greenlet 在运行，而不是等待 IO。

因此结合 gunicorn 启动服务的命令可设置为：`gunicorn manage:app -b 0.0.0.0:8080 -w 4 --worker-class gevent`（此命令可写入 supervisor 的应用配置文件中）
