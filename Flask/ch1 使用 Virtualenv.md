# 使用 virtualenv 虚拟环境

virtualenv 是 Python 的虚拟环境，可以在同一台 PC 上隔离不同的开发环境。主要用于为不同的项目构建独立与隔离的三方库依赖。

1. 在系统中安装 virtualenv：`pip install virtualenv`
2. 在项目目录中建立 virtualenv 虚拟环境：`virtualenv [环境名]` 
3. 启动虚拟环境：
	- `env_dir\Scripts\activate`(Windows)
	- `# source env_dir/bin/activate`(Linux)
4. 退出虚拟环境： `deactivate`

## 需求文件的创建及使用

Python项目中往往必须包含一个 requirements.txt 文件，用于记录所有依赖包及其精确的版本号，以便在新环境中部署。

在虚拟环境中使用 pip 生成需求文件：

> `(venv) $ pip freeze > requirements.txt`

安装或升级包后，最好更新该文件。

按照需求文件上的所列项，安装依赖包：

> `(venv) $ pip install -r requirements.txt`
