<p align="center">
    <img src="https://github.com/open-cmdb/cmdb/blob/dev/images/cmdb-0.png">
</p>

# cmdb

> CMDB 资产管理系统

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![pyversions](https://img.shields.io/badge/python%20-3.5%2B-blue.svg)
![vueversions](https://img.shields.io/badge/Vue.js-2.3.4-4fc08d.svg)
![es2015](https://img.shields.io/badge/ECMAScript-6-green.svg)
![element ui](https://img.shields.io/badge/element-2.1.0-20a0ff.svg)

## 知乎链接
https://zhuanlan.zhihu.com/p/34191320

## 在线演示
http://cmdb.xyz
用户名：admin  密码：cmdbcmdb (请不要修改)

## 问答群
<p align="center">
    <img src="https://github.com/open-cmdb/cmdb/blob/master/images/cmdb-weichat-QR.png">
</p>

## 特性
* 热添加删除表 自定义字段类型
* REST前后端分离架构 开放所有API接口
* 强大的搜索查找能力（后端使用elasticsearch存储数据 ） 可以配合kibana使用
* 支持查看数据修改记录
* 表级权限管理
* 容器快速部署

### 前端

* Vue
* Element-ui
* Vue-Router
* Vuex
* Axios

### 后端

* Python3
* Django 1.11
* Django REST framework
* Elasticsearch
* Mysql
* LDAP
* uwsgi
* Nginx
* Docker

## 前端
https://github.com/open-cmdb/cmdb-web

## 快速开始


准备一台可以访问互联网的centos服务器（内存大于等于4G） 将下面代码保存到install_cmdb.py  执行sudo python install_cmdb.py
```python
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import subprocess
import argparse
import time

def base(cmd):
    if subprocess.call(cmd, shell=True):
        raise Exception("{} 执行失败".format(cmd))

def install_docker():
    base("sudo yum install -y yum-utils device-mapper-persistent-data lvm2")
    base("sudo yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo")
    base("sudo yum makecache fast")
    base("sudo yum -y install docker-ce")
    if(not os.path.exists("/etc/docker")):
        base("mkdir -p /etc/docker")
    with open("/etc/docker/daemon.json", "w") as f:
        f.write('{\n    "registry-mirrors": ["https://9f4w4icn.mirror.aliyuncs.com"] \n}')
    base("sudo systemctl daemon-reload")
    base("sudo systemctl start docker")

def create_dir():
    if (not os.path.exists("/var/cmdb/db")):
        base("sudo mkdir -p /var/cmdb/db")
    if (not os.path.exists("/var/cmdb/es")):
        base("sudo mkdir -p /var/cmdb/es")

def run_db_container():
    base("sudo docker run --name cmdb-db -d -e MYSQL_ROOT_PASSWORD=cmdbcmdb -v /var/cmdb/db:/var/lib/mysql mysql:5.7.21")

def run_es_container():
    base("sudo docker run --name cmdb-es -d -v /var/cmdb/es:/usr/share/elasticsearch/data elasticsearch:5.6.8")

def init_db():
    base("sudo docker run -it --rm --link cmdb-db -e DB_HOST=cmdb-db -e ENV=PRO -e DB_PORT=3306 -e DB_USERNAME=root -e DB_PASSWORD=cmdbcmdb -e DB_NAME=cmdb mingmingtang/cmdb init-db")

def run_cmdb_container(site_url, email_host, email_port, email_username, email_password):
    base("sudo docker run -d --name cmdb --link cmdb-db --link cmdb-es -p 80:80 -e ENV=PRO -e SITE_URL={} -e DB_HOST=cmdb-db -e DB_PORT=3306 -e DB_USERNAME=root -e DB_PASSWORD=cmdbcmdb -e DB_NAME=cmdb -e ELASTICSEARCH_HOSTS=cmdb-es -e EMAIL_HOST={} -e EMAIL_PORT={} -e EMAIL_USERNAME={} -e EMAIL_PASSWORD={} mingmingtang/cmdb start".format(site_url, email_host, email_port, email_username, email_password))

def input_para(help):
    value = ""
    while(not value):
        value = raw_input(help)
    return value

if __name__ == '__main__':
    if(os.geteuid() != 0):
        raise("请以root权限运行")
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--siteurl", type=str, help="E.g: http://cmdb.xxx.com, http://172.17.100.1")
    # parser.add_argument("--emailhost", type=str, help="E.g: http://cmdb.xxx.com, http://172.17.100.1")
    # parser.add_argument("--emailport", type=str, help="E.g: http://cmdb.xxx.com, http://172.17.100.1")
    # parser.add_argument("--emailusername", type=str, help="E.g: http://cmdb.xxx.com, http://172.17.100.1")
    # parser.add_argument("--emailpassword", type=str, help="E.g: http://cmdb.xxx.com, http://172.17.100.1")
    # args = parser.parse_args()
    # SITE_URL = args.SITE_URL

    site_url = input_para("请输入网站域名或IP（http://cmdb.xxx.com）：")
    email_host = input_para("网站邮箱服务器（smtp.163.com）：")
    email_port = input_para("邮箱服务器端口（25）：")
    email_username = input_para("邮箱用户名（cmdb@163.com）：")
    email_password = input_para("邮箱密码|独立授权码（P@ssw0rd）：")

    print("开始安装docker")
    install_docker()
    print("开始创建目录")
    create_dir()
    print("开始运行mysql容器")
    run_db_container()
    print("开始运行elasticsearch容器")
    run_es_container()
    print("等待数据库启动完成(10s)")
    time.sleep(10)
    print("开始初始化数据库")
    init_db()
    print("开始运行cmdb")
    run_cmdb_container(site_url, email_host, email_port, email_username, email_password)
    print("完成！")
```

## 手工部署
先安装好Elasticsearch(5.6) 和 Mysql(5.7) 其它版本未测试

### 容器名称
mingmingtang/cmdb

### 初始化数据库
```bash
docker run -it --name cmdb-init-db --rm -e DB_HOST=数据库地址 -e ENV=PRO -e DB_PORT=数据库端口 -e DB_USERNAME=数据库用户名 -e DB_PASSWORD=数据库密码 -e DB_NAME=cmdb mingmingtang/cmdb init-db
```
示例：
```bash
docker run -it --name cmdb-init-db --rm -e DB_HOST=172.16.0.11 -e ENV=PRO -e DB_PORT=3306 -e DB_USERNAME=root -e DB_PASSWORD=******** -e DB_NAME=cmdb mingmingtang/cmdb init-db
```

### 运行CMDB
```bash
docker run -d --name cmdb -p 80:80 -e ENV=PRO -e SITE_URL=网站地址 -e DB_HOST=数据库地址 -e DB_PORT=数据库端口 -e DB_USERNAME=数据库用户名 -e DB_PASSWORD=数据库密码 -e DB_NAME=cmdb -e ELASTICSEARCH_HOSTS=ES地址，多个用英文逗号隔开，格式http://xx.xx.xx.xx:9200 -e EMAIL_HOST=邮箱smtp地址 -e EMAIL_PORT=邮箱smtp端口 -e EMAIL_USERNAME=发件箱 -e EMAIL_PASSWORD=邮箱密码 mingmingtang/cmdb start
```
示例：
```bash
docker run -d --name cmdb -p 80:80 -e ENV=PRO -e SITE_URL=http://120.79.60.130 -e DB_HOST=172.16.0.11 -e DB_PORT=3306 -e DB_USERNAME=root -e DB_PASSWORD=******** -e DB_NAME=cmdb -e ELASTICSEARCH_HOSTS=http://127.0.0.1:9200 -e EMAIL_HOST=smtp.163.com -e EMAIL_PORT=25 -e EMAIL_USERNAME=mmt_cmdb@163.com -e EMAIL_PASSWORD=******** mingmingtang/cmdb start
```

## 嘿 哥们儿 给颗星吧 ┭┮﹏┭┮
