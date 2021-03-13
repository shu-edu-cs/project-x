# 上大共享图书

## 部署

### 数据库

在Linux下，使用命令安装MySQL

```shell
yum install mysql-server
```

启动MySQL访问

```
/etc/init.d/mysqld restart
```

进入MySQL

```
mysql
```

设置root用户密码

```
set password = password('root');
```

连接到MySQL后，创建名为ShareBook的数据库。

执行光盘文件中的数据库SQL，可自动插入表结构和测试数据。

### 环境安装

安装Python 3.8 及以上版本，Linux环境建议使用pyenv部署。

### 创建虚拟环境

使用venv指令来创建一个虚拟环境。

```shell
python -m venv /path/to/new/virtual/environment
```

更详细的操作可见Python官方文档： https://docs.python.org/zh-cn/3.6/library/venv.html

### 安装依赖包

使用pip install 命令，安装依赖包

```shell
pip install -r requirements.txt
```

### 配置环境变量

为保障数据安全，部分敏感配置，如MySQL配置，需要配置在环境变量中。

| 环境变量       | 说明            | 示例        |
| -------------- | --------------- | ----------- |
| PROJECT_X_USER | MySQL数据库账户 | root        |
| PROJECT_X_PASS | MySQL数据库密码 | password123 |
| PROJECT_X_HOST | MySQL服务器地址 | 127.0.0.0   |

也可以修改配置文件 projectx/settings.py 的相关配置，将os.environ.get('PROJECT_X_USER')等从环境变量读取配置的地方，直接修改为数据库的连接配置即可。

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sharebook',
        'USER': os.environ.get('PROJECT_X_USER'),
        'PASSWORD': os.environ.get('PROJECT_X_PASS'),
        'HOST': os.environ.get('PROJECT_X_HOST'),
        'PORT': '3306',
    }
}
```

### 激活虚拟环境

假设虚拟环境所在目录为venv

#### Linux

```shell
$ cd venv
$ source bin/activate
```

#### Windows

```powershell
venv\Scripts\activate
```

### 启动访问

使用命令启动站点

```
python manage.py runserver
```

### 访问站点

打开浏览器，访问 http://127.0.0.1:8000/

### 登录系统

测试账号密码：

admin/4EPzKLnn8GF4Vy

student/E5NFR98iyNVwXX

