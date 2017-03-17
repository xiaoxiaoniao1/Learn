# Flask 常用扩展插件
仅仅靠 Flask 基础库的功能是不够的，Flask 拥有多种扩展插件来实现各种模块化的功能。以下按照常用的配置目录，来介绍 Flask 中较为常见的功能插件。

## Flask-SQLAlchemy
一个从模型到数据库的映射框架，在 Flask 中提供了模型以及数据库操作。

### 初始化应用
```
# app/init.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

# 由于是全局的实例，此后其他模块引入需SQLAlchemy时只需引入db即可
db = SQLAlchemy() 

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
```

### 模型声明
```
# app/models.py
from . import db

class User(db.Model):
    __tablename__ = 'users'   # 将创建的数据库的实际表名
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email
```

详细的模型关系说明请看 [Flask sqlalchemy 数据库操作文档](https://github.com/xuelangZF/ehpc/wiki/Flask-sqlalchemy-%E6%95%B0%E6%8D%AE%E5%BA%93%E6%93%8D%E4%BD%9C%E6%96%87%E6%A1%A3) 。


## Flask-Script 与 Flask-Migrate
Flask-Script 为 Flask 提供了可通过外部脚本使用命令行运行程序的功能，如启动服务、数据库迁移、在环境上下文中启动 shell 等。而 Flask-Migrate 用于进行数据库迁移。
```
# manage.py

import os
from app import app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
```

数据库迁移的命令主要包括：

- 初始化迁移库：`# python manage.py db init`
- 创建迁移脚本：`# python manage.py db migrate`
- 更新数据库：`# python manage.py db upgrade`

## MySQL-python 
MySQL-python 是 python 环境与 mysql 数据库的底层交互接口。作为一个必需库，在安装时经常会遇到安装失败的情况。因此一般是在 windows 开发环境下使用 exe 进行安装后再把库文件复制到已部署项目的虚拟环境中。

在 centos 系统中使用 pip 安装 MySQL-python 时遇到的一些问题的解决方法：

1. 执行`pip install mysql-python`时，报错 `EnvironmentError: mysql_config not found` ，解决方法为：`yum install mysql-devel`
2. 再次执行`pip install mysql-python`安装时，仍然报错`error: command 'gcc' failed with exit status 1`， 解决方法：`yum install gcc python-devel`

### 参考文章
[centos下pip安装mysql_python](http://www.cnblogs.com/yangxia-test/p/4691947.html)


## Flask-Login
Flask-Login 为 Flask 提供了会话管理。它处理日常的登入、登出并长期保留用户会话。

### 初始化应用
Flask-Login 最重要的部分就是登录管理器类 LoginManager ，实例化后对应用进行初始化。
```
# app/init.py

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)

#设置会话保护强度：None、"basic" 或 "strong"
login_manager.session_protection = 'strong'
#设置登录视图
login_manager.login_view = 'user.signin'  
```

### 相关配置
需要设置一个 user_loader 回调函数，这个函数用于从会话中存储的用户 ID 重新加载用户对象（注意：如果 ID 无效，它应该返回 None，而不是抛出异常），如：
```
@login_manager.user_loader
def load_user(userid):
    return User.get(userid)
```

### 使用方法
当用户通过验证后，用 login_user 函数来登入他们：
```
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", form=form)
```

可以通过 current_user 代理访问当前会话中已登录的用户。但当用户未登录时，current_user 被设置为一个 AnonymousUser 对象，它包含下列属性： 

- is_active 和 is_authenticated 返回 False 
- is_active 返回 True 
- get_id 返回 None。

需要用户登入的视图可以用 login_required 装饰器来装饰，被 login_required 装饰器拦截的请求会跳转到登录视图。当重定向到登入视图，请求字符串中往往会额外设置一个 next 变量，值为用户之前试图访问的页面。
```
@app.route("/settings")
@login_required
def settings():
    pass
```

当用户要登出时：
```
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(somewhere)
```

## Flask_Babel
Flask_Babel 是 Flask 的翻译扩展工具，可配置指定文字的翻译文本。

### 初始化应用
使用命令`$ pip install Flask-Babel`进行安装。

在完成 app 的基本配置初始化后，使用 Babel 对 app 进行初始化：
```
from flask import Flask
from config import config
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object(config[config_name])
babel = Babel(app)
```

### 配置参数
首先在 app 的 config 中设置 Babel 的配置参数，分别代表翻译文本的默认语言以及其默认时区。
```
BABEL_DEFAULT_LOCALE = 'zh'
BABEL_DEFAULT_TIMEZONE = 'CST'
```

在 app 目录下创建配置文件 babel.cfg，用于设置 babel 要从哪些位置搜索需翻译的字符串：
```
[python: **.py]
[jinja2: **/templates/**.html]
extensions=jinja2.ext.autoescape,jinja2.ext.with_
```

### 生成翻译模板
使用`# pybabel extract -F babel.cfg -o messages.pot .`命令生成翻译模板`messages.pot`。该模板自动查找 babel.cfg 中所配置的区域中需要翻译的字符串。

### 创建翻译文本
使用`# pybabel init -i messages.pot -d translations -l zh`创建中文翻译。这句命令会在 app 主目录中生成一个 translations 目录。要确保 flask 能找到翻译内容，translations 目录要和 templates 目录在同一个目录中。接下来我们就可以进行翻译了，修改 `translations/zh_Hans_CN/LC_MESSAGES/messages.po`文件添加翻译文本。

### 编译
翻译完后执行命令`# pybabel compile -d translations`进行编译，编译结果为 message.mo 文件。编译成功后，即可在应用的网页上看到翻译后的文本。

### 修改翻译
有时我们需要对程序和模板做修改，翻译也要随之更新。更新后需要用前面的命令重新生成 messages.pot 文件，然后使用命令`# pybabel update -i messages.pot -d translations`将更新的内容 merge 到原来的翻译中，最后再到对应 locale 的文件夹下更新翻译并 compile 即可。

若只是修改翻译文本而未更改程序和模板，则只需修改 messages.po 文件里的文本后重新编译即可。

## Flask-Mail
Flask-Mail 用于自动发送邮件。

### 初始化应用
```
# app/init.py
from flask_mail import Mail

mail = Mail()
mail.init_app(app)
```

### 参数配置
可参考 [Flask-Mail 文档](http://www.pythondoc.com/flask-mail/index.html) 进行如下内置参数配置：
```
# config.py

# If use QQ email, please see http://service.mail.qq.com/cgi-bin/help?id=28 firstly.
MAIL_SERVER = 'smtp.sina.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'milanlanlanlan@sina.com'
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '1970025901a'
```

除了设置参数以外，还应当确保邮件服务器可提供服务。

### 发送邮件

为了能够发送邮件，首先需要创建一个 Message 实例:

```
from flask_mail import Message
@app.route("/")
def index():
    msg = Message("Hello",     # 此处构造函数的首个参数的值"Hello"是邮件标题
                  sender="from@example.com",
                  recipients=["to@example.com"]) 
```

可设置一个或者多个收件人:
```
msg.recipients = ["you@example.com"]
msg.add_recipient("somebodyelse@example.com")
```
若设置了 MAIL_DEFAULT_SENDER，就不必再次填写发件人，默认情况下将会使用配置项的发件人。

邮件内容可以直接包含 body 或者包含 HTML:
```
msg.body = "testing"
msg.html = "<b>testing</b>"
```

最后，发送邮件的时候请使用 Flask 应用设置的 Mail 实例:`mail.send(msg)`

## 自定义模板过滤器

为了使视图层和控制层解耦，往往使用自定义的模板过滤器，而不是在控制层中增加逻辑。

``` 
# app/util/init.py
from flask import Blueprint
filter_blueprint = Blueprint('filters', __name__)

# Register all the filter.
# 往往不是把所有过滤器写入同一个文件中，而是分多个文件，然后在本文件中用 import 引用。
@filter_blueprint.app_template_filter('reversel')
def reverse_filter(s):
    return s[::-1]