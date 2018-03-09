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
    base("sudo docker run -it --rm --link cmdb-db -e DB_HOST=cmdb-db -e DB_PORT=3306 -e DB_USERNAME=root -e DB_PASSWORD=cmdbcmdb -e DB_NAME=cmdb mingmingtang/cmdb init-db")

def run_cmdb_container(site_url, email_host, email_port, email_username, email_password):
    base("sudo docker run -d --name cmdb --link cmdb-db --link cmdb-es -p 80:80 -e SITE_URL={} -e DB_HOST=cmdb-db -e DB_PORT=3306 -e DB_USERNAME=root -e DB_PASSWORD=cmdbcmdb -e DB_NAME=cmdb -e ELASTICSEARCH_HOSTS=cmdb-es -e EMAIL_HOST={} -e EMAIL_PORT={} -e EMAIL_USERNAME={} -e EMAIL_PASSWORD={} mingmingtang/cmdb start".format(site_url, email_host, email_port, email_username, email_password))

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