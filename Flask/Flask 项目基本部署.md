# Flask 项目基本部署

Flask 项目没有固定的目录配置，因此在此介绍一个对 Flask 进行基本部署的教程。

## 环境安装
首先使用 virtualenv 构建好虚拟的 python 依赖环境，并安装必要的 Flask 依赖包，比如：

- flask：Flask 框架的基础库
- mysql-python：处理与数据库的底层交互
- SQLAlchemy：一个 ORM 框架，用于处理数据库与对象之间的映射
- Flask-SQLAlchemy：简化在 Flask 中 SQLAlchemy 的 使用
- Flask-Script：为 Flask 程序提供了命令行模式
- Flask-Migrate：数据库迁移工具
- Flask-Login：封装用户会话管理

其他功能性的扩展插件可选择安装，比如：

- flask-mail：用于管理邮件自动发送
- Flask-babel：实现语言互相转换的翻译工具
- Werkzeug： 计算密码散列值并进行核对
- Flask-WTF： Web 表单

## 目录结构
初始目录结构如下图所示：

![初始目录配置图](https://cloud.githubusercontent.com/assets/22606175/23286448/9f0c3b46-fa72-11e6-87d7-b90f25452eec.jpg)

- Flask 程序一般都保存在名为 app 的文件夹中
- migrations 文件夹包含数据库迁移脚本
- venv 文件夹包含 Python 虚拟环境
- requirements.txt 列出了所有依赖包，便于项目迁移时重新生成相同的虚拟环境；
- config.py 存储配置参数，如数据库账户密码等
- manage.py 用于通过命令行启动程序的脚本

## 配置文件详解

### config.py
config.py 是初始化 Flask app 的配置文件，主要包括多种模式下的配置类型和全局参数（如密钥、连接数据库的 URL） 等。此外需注意的是，敏感数据不能直接写入，应从操作系统的环境变量中读取。
```
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    def __init__(self):
        pass
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    def __init__(self):
        pass
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DEV_DATABASE_URL') or
                               'mysql://root:123456@localhost/lancs')

class ProductionConfig(Config):
    def __init__(self):
        pass
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DEV_DATABASE_URL') or
                               'mysql://root:123456@localhost/lancs')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

### app/init.py
app/init.py 是程序包的构造文件，主要包括创建 flask app 的工厂函数。配置 Flask 扩展插件时往往在工厂函数中对 app 进行相关的初始化。
```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    # Register all the filter.
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
```

### manage.py
manage.py 是使用命令行启动服务进程、数据库迁移的脚本文件。
```
import os
from Lancs import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('LANCS_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
```


