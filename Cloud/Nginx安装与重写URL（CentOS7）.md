# Nginx安装与重写URL（CentOS7）
## Nginx安装
新建 /etc/yum.repos.d/nginx.repo：
```
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/7/$basearch/
gpgcheck=0
enabled=1
```

使用命令`# yum install nginx`安装nginx。安装完成后使用命令`# nginx`启动 nginx 。使用`# nginx -v`查看 nginx 版本。并可通过在浏览器里直接访问机器的IP地址可查看 nginx 是否启动成功（**需确保关闭 CentOS 的 SELinux 和防火墙服务**）。

## 重写URL
使用`# nginx -t`命令查看当前 nginx 配置文件状态以及路径。在配置文件中的项 http{} 里可重写URL：
```
server{
        listen 80;                  #设置监听端口
        server_name 172.18.216.123; #决定配置哪几台服务器，值可为域名也可为IP地址
        location / {                #对匹配目录"/"进行操作。也可设置为其它的目录
            rewrite / http://www.baidu.com break; #执行URL重写，支持正则表达式
        }
}
```

也可在配置文件的 server 块中写，此时是针对该服务器的全局配置。如：
```
server {
    rewrite 规则 定向路径 重写类型;
}
```
 - 规则：可以是字符串或者正则来表示想匹配的目标url
 - 定向路径：表示匹配到规则后要定向的路径，如果规则里有正则，则可以使用 $index 来表示正则里的捕获分组
 - 重写类型：
     - last ：匹配重写后的URL，再一次对URL重写规则进行匹配。浏览器地址栏URL地址不变
     - break；匹配重写URL后终止匹配，直接使用。浏览器地址栏URL地址不变
     - redirect：返回302临时重定向，浏览器地址会显示跳转后的URL地址
     - permanent：返回301永久重定向，浏览器地址栏会显示跳转后的URL地址

更多具体语法可参见官方文档 [Rewrite模块](http://nginx.org/en/docs/http/ngx_http_rewrite_module.html) 或中文技术博客 [Nginx配置URL重写](http://www.tuicool.com/articles/qEzMNrI)。