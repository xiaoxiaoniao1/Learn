# 使用 virtualenv 虚拟环境

virtualenv 是 Python 的虚拟环境，可以在同一台 PC 上隔离不同的开发环境。主要用于为不同的项目构建独立与隔离的三方库依赖。

1. 在系统中安装 virtualenv：`pip install virtual`
2. 在项目目录中建立 virtualenv 虚拟环境：`virtualenv [环境名]` 
3. 启动虚拟环境：
	- `env_dir\Scripts\activate`(Windows)
	- `# source env_dir/bin/activate`(Linux)
4. 退出虚拟环境： `deactivate`

