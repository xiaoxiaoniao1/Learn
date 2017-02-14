# 部署Ceph集群(CentOS7环境)
本文档说明如何在 CentOS 虚拟机上部署一个 ceph-deploy 管理节点和一个三节点的 Ceph 存储集群。

![Ceph集群架构](http://docs.ceph.org.cn/_images/ditaa-cffd08dd3e192a5f1d724ad7930cb04200b9b425.png)

*经实践，能够顺利地在实验室云平台上部署，但在超算中心提供的云环境中总是卡死在软件更新这一步而无法部署成功。*
## 准备阶段
1. 在四台虚机上均安装同一版本的 CentOS7 操作系统（参考本文档同一目录下的[《配置虚拟云主机》](https://github.com/Zouzhp3/Learn/blob/master/Openstack/%E9%85%8D%E7%BD%AE%E8%99%9A%E6%8B%9F%E4%BA%91%E4%B8%BB%E6%9C%BA(CentOS).md)）。所有虚机开启网络服务、更改主机名、并更换 yum 源为国内镜像站（若默认源速度快的话也可以不更换 yum 源）。

2. 更新所有虚机上的 /etc/hosts 文件，以便用于解析子网内所有虚机的主机名：
> 在/etc/hosts 中增加所有虚机的“ IP地址 域名 主机名 ”格式的条目，如：`172.18.216.211 mon.localdomain mon`

3. 所有虚机都安装 NTP 服务（用于同步所有虚机的时钟，以免时钟漂移导致故障）：`sudo yum install ntp ntpdate ntp-doc`。并确认所有虚机是否都已开启 SSH 服务：`service sshd status`。

4. 关闭所有虚机的 SELinux：编辑 /etc/selinux/config ，设置SELINUX = disabled； 执行`# setenforce 0`可即时生效。可使用`# getenforce`命令查看SELinux状态。

5. 关闭所有虚机的防火墙服务：

 ```
 # systemctl stop firewalld
 # systemctl disable firewalld
 ```

## 预检阶段
### 安装 Ceph 部署工具
把 Ceph 仓库添加到 ceph-deploy 管理节点，然后安装 ceph-deploy 。

下载 EPEL (Extra Packages for Enterprise Linux)：
```
sudo yum install -y yum-utils && sudo yum-config-manager --add-repo https://dl.fedoraproject.org/pub/epel/7/x86_64/ && sudo yum install --nogpgcheck -y epel-release && sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7 && sudo rm /etc/yum.repos.d/dl.fedoraproject.org*
```
这个源可能比较下载速度很慢，也可以直接使用`yum install --nogpgcheck -y epel-release`命令。

把软件包源加入软件仓库。用文本编辑器创建一个 YUM库文件，其路径为 /etc/yum.repos.d/ceph.repo 。
例如：`# sudo vim /etc/yum.repos.d/ceph.repo`

粘贴如下内容，用 Ceph 的最新主稳定版名字替换 {ceph-stable-release} （如 firefly ），用虚机的Linux发行版名字替换 {distro} （如 el6 为 CentOS 6 、 el7 为 CentOS 7 、 rhel6 为 Red Hat 6.5 、 rhel7 为 Red Hat 7 、 fc19 是 Fedora 19 、 fc20 是 Fedora 20 ）。最后保存到 /etc/yum.repos.d/ceph.repo 文件中。

```
[ceph-noarch]
name=Ceph noarch packages
baseurl=http://download.ceph.com/rpm-{ceph-release}/{distro}/noarch
enabled=1
gpgcheck=1
type=rpm-md
gpgkey=https://download.ceph.com/keys/release.asc
```
更新软件库并安装 ceph-deploy ：
```
# sudo yum update
# sudo yum install ceph-deploy
```
PS:有些系统执行`yum update`要更新多达上千的包（更新过程中可能卡死），而有些系统只需更新一百左右，可能与系统版本新旧有关。

注意：`yum update`命令很重要，如果不更新可能在后面部署集群时会造成安装 Ceph 失败的问题。
### 创建部署 Ceph 的系统用户
ceph-deploy 工具必须以系统普通用户登陆 Ceph 节点，且此用户需拥有无密码使用`sudo`的权限（因为它需要在安装软件及配置文件的过程中不必输入密码）。

 **建议**在集群内的所有 Ceph 节点上给 ceph-deploy 创建一个特定的用户（全集群统一的用户名可简化操作），但**不要**使用 “ ceph ” 作为用户名。

 ```
 # ssh user@ceph-server
 # sudo useradd -d /home/{username} -m {username}
 # sudo passwd {username}
 ```
其中user@ceph-server为SSH所连接的节点（如root@mon），{username}为所设置的同一用户名。

确保各 Ceph 节点上新创建的用户都有 sudo 权限：

 ```
 # echo "{username} ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/{username}
 # sudo chmod 0440 /etc/sudoers.d/{username}
 ```

### 允许无密码 SSH 登录
因为 ceph-deploy 不支持输入密码，所以必须在管理节点上生成 SSH 密钥并把其公钥分发到各 Ceph 节点。 ceph-deploy 会尝试给初始 monitors 生成 SSH 密钥对。

生成 SSH 密钥对，**但不要用 sudo 或 root 用户**。提示 “Enter passphrase” 时，直接回车，口令即为空：

```
# ssh-keygen

Generating public/private key pair.
Enter file in which to save the key (/ceph-admin/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /ceph-admin/.ssh/id_rsa.
Your public key has been saved in /ceph-admin/.ssh/id_rsa.pub.
```
把公钥拷贝到各 Ceph 节点，把下列命令中的 {username} 替换成前面创建部署 Ceph 的用户里的用户名。
```
# ssh-copy-id {username}@node1
# ssh-copy-id {username}@node2
# ssh-copy-id {username}@node3
```

用该用户名ssh到另外节点上的该用户名，若无需密码即可成功连接，则说明设置成功。

## 创建存储集群
以上一节中所创建的部署用户的身份，在管理节点上创建目录`mkdir my-cluster`，用于保存 ceph-deploy 生成的配置文件和密钥对。由于 ceph-deploy 会把文件输出到当前目录，所以请**确保在此目录下执行 ceph-deploy **。

**注意**：在某些发行版（如 CentOS ）上，执行 ceph-deploy 命令时，如果 Ceph 节点默认设置了 requiretty 那就会遇到报错：“抱歉，您必须拥有一个终端来执行 sudo”。可以这样禁用此功能：对**所有节点**执行`sudo visudo`，找到"Defaults requiretty"并将其注释掉，这样 ceph-deploy 就能用部署用户的身份登录并使用 sudo 了。

如果在某些地方碰到麻烦，想从头再来，可以用下列命令清除配置：
```
ceph-deploy purgedata {ceph-node} [{ceph-node}]
ceph-deploy forgetkeys
```
用下列命令可以连 Ceph 安装包一起清除（但如果执行了 purge ，则必须重新安装 Ceph ）：
```
ceph-deploy purge {ceph-node} [{ceph-node}]
```

在管理节点上，进入刚创建的放置配置文件的目录，用 ceph-deploy 执行如下步骤：

1. 创建集群：`ceph-deploy new {initial-monitor-node(s)}`,其中{initial-monitor-node(s)}是监控节点的主机名。在当前目录下用 ls 检查 ceph-deploy 的输出，应该有一个 Ceph 配置文件、一个 monitor 密钥环和一个日志文件。
2. 把 Ceph 配置文件里的默认副本数从 3 改成 2 ，这样只有两个 OSD 也可以达到 active + clean 状态。把下面这行加入 [global] 段：`osd pool default size = 2`。
3. 在各节点安装 ceph ：`ceph-deploy install {ceph-node} [{ceph-node} ...]`,如： `ceph-deploy install admin mon osd0 osd1`。**注意**，此处可能会遇到报错：“RuntimeError: NoSectionError: No section: 'ceph'”，但只需执行`yum remove ceph-release`即可。
4. 配置初始 monitor(s)、并收集所有密钥：`ceph-deploy mon create-initial`。

完成上述操作后，当前目录里应该会出现这些密钥环：
```
{cluster-name}.client.admin.keyring
{cluster-name}.bootstrap-osd.keyring
{cluster-name}.bootstrap-mds.keyring
{cluster-name}.bootstrap-rgw.keyring
```

之后再继续部署两个OSD：

1. 登录到 Ceph 节点、并给 OSD 守护进程创建一个目录。
 ```
ssh node2
sudo mkdir /var/local/osd0
exit

ssh node3
sudo mkdir /var/local/osd1
exit
```
2. 从管理节点执行 ceph-deploy 来准备 OSD ：`ceph-deploy osd prepare {ceph-node}:/path/to/directory`，如：`ceph-deploy osd prepare osd0:/var/local/osd0 osd1:/var/local/osd1`。
3. 激活 OSD ：`ceph-deploy osd activate {ceph-node}:/path/to/directory`，如：`ceph-deploy osd activate osd0:/var/local/osd0 osd1:/var/local/osd1`。注意：此处可能报错“ERROR: error creating empty object store in /var/local/osd0: (13) Permission denied”，解决方法是在各个节点上给/var/local/osd1/和/var/local/osd1/添加权限：
 
 ```
chmod 777  /var/local/osd0/
chmod 777  /var/local/osd0/*
chmod 777  /var/local/osd1/
chmod 777  /var/local/osd1/*
```

用 ceph-deploy 把配置文件和 admin 密钥拷贝到管理节点和 Ceph 节点，这样每次执行 Ceph 命令行时就无需指定 monitor 地址和 ceph.client.admin.keyring 了：`ceph-deploy admin {admin-node} {ceph-node}`，如：`ceph-deploy admin admin mon osd0 osd1`。

确保你对 ceph.client.admin.keyring 有正确的操作权限：`sudo chmod +r /etc/ceph/ceph.client.admin.keyring`。

检查集群的健康状况：`ceph health`，若为“HEALTH_OK”则说明部署成功。

## 测试：定位某个对象
作为练习，我们先创建一个对象，用 rados put 命令加上对象名、一个有数据的测试文件路径、并指定存储池(**在新安装好的集群上，只有一个名为 "rbd" 的存储池**，用`ceph osd lspools`命令可列出集群的存储池)。例如：
 ```
echo {Test-data} > testfile.txt
rados put {object-name} {file-path} --pool=rbd
rados put test-object-1 testfile.txt --pool=rbd
```
为确认 Ceph 存储集群存储了此对象，可执行：
 ```
rados -p rbd ls
```
现在，定位对象：
 ```
ceph osd map {pool-name} {object-name}
ceph osd map rbd test-object-1
```
Ceph 应该会输出对象的位置，例如：
 ```
osdmap e537 pool 'data' (0) object 'test-object-1' -> pg 0.d1743484 (0.4) -> up [1,0] acting [1,0]
```
用`rados rm`命令可删除此测试对象，例如：
 ```
rados rm test-object-1 --pool=rbd
```
## 参考文档
[Ceph官方文档](http://docs.ceph.com/docs/master/)

[Ceph官方文档中文版](http://docs.ceph.org.cn/)

[博客：Ceph搭建过程中遇到的各种问题](http://blog.csdn.net/sinat_36023271/article/details/52402028)
