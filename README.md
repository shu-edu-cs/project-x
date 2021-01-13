# 上大共享图书

## 前言

TODO

## 部署

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

