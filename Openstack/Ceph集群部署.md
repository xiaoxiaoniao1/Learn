# 部署Ceph集群(CentOS7环境)
本文档说明如何在 CentOS 虚拟机上部署一个 ceph-deploy 管理节点和一个三节点的 Ceph 存储集群。

![Ceph集群架构](http://docs.ceph.org.cn/_images/ditaa-cffd08dd3e192a5f1d724ad7930cb04200b9b425.png)

## 准备阶段
1. 在四台虚机上均安装同一版本的 CentOS7 操作系统（参考本文档同一目录下的[《配置虚拟云主机》](https://github.com/Zouzhp3/Learn/blob/master/Openstack/%E9%85%8D%E7%BD%AE%E8%99%9A%E6%8B%9F%E4%BA%91%E4%B8%BB%E6%9C%BA(CentOS).md)）。所有虚机开启网络服务、更改主机名、并更换yum源为国内镜像站。

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

更新管理节点上的仓库，并安装 ceph-deploy：
```
sudo yum install -y yum-utils && sudo yum-config-manager --add-repo https://dl.fedoraproject.org/pub/epel/7/x86_64/ && sudo yum install --nogpgcheck -y epel-release && sudo rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7 && sudo rm /etc/yum.repos.d/dl.fedoraproject.org*
```
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

生成 SSH 密钥对，但不要用 sudo 或 root 用户。提示 “Enter passphrase” 时，直接回车，口令即为空：

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
