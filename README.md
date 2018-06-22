# README.md

## Developer

1. daijinru@weilaigongzuo.com

## Dependence

| Package | Version |
| :---: | :---: |
| Python | 3.6.5 |
| Flask | 1.0.2 |
| Pymongo | 3.6.1 |
| MongoDB | 3.4.4 |
| virtualenv | 16.0.0 |

## Operation

如果是在新环境，请先执行脚本导入数据

```
$ cd scripts
$ python3 resource_build.py
```

项目根目录创建虚拟环境文件夹

```
$ virtualenv -p python3 venv
```

启动虚拟环境

```
$ . venv/bin/activate
```

安装 Flask

```
(venv) $ pip3 install flask
```

安装 Pymongo

```
(venv) $ pip3 install pymongo
```

启动项目

```
(venv) $ python3 run.py
```

## Dictionaries

| Name | Desc |
| :--: | :--: |
| collection | Mongo 中的集合，对应技术栈，例如 Javascript,Css |
| document | 集合中的文档，例如 Css 中的 Flexbox,Grid |
| token | 身份认证 |