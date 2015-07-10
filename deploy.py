#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
from http://www.coder4.com/archives/4303
"""

from datetime import datetime
from fabric.api import *

# 登录用户和主机名：
env.user = 'root'
env.hosts = ['www.example.com'] # 如果有多个主机，fabric会自动依次部署

def pack():
    ' 定义一个pack任务 '
    # 打一个tar包：
    tar_files = ['*.py', 'static/*', 'templates/*', 'favicon.ico']
    local('rm -f example.tar.gz')
    local('tar -czvf example.tar.gz --exclude=\'*.tar.gz\' --exclude=\'fabfile.py\' %s' % ' '.join(tar_files))

def deploy():
    ' 定义一个部署任务 '
    # 远程服务器的临时文件：
    remote_tmp_tar = '/tmp/example.tar.gz'
    tag = datetime.now().strftime('%y.%m.%d_%H.%M.%S')
    run('rm -f %s' % remote_tmp_tar)
    # 上传tar文件至远程服务器：
    put('shici.tar.gz', remote_tmp_tar)
    # 解压：
    remote_dist_dir = '/srv/www.example.com@%s' % tag
    remote_dist_link = '/srv/www.example.com'
    run('mkdir %s' % remote_dist_dir)
    with cd(remote_dist_dir):
        run('tar -xzvf %s' % remote_tmp_tar)
    # 设定新目录的www-data权限:
    run('chown -R www-data:www-data %s' % remote_dist_dir)
    # 删除旧的软链接：
    run('rm -f %s' % remote_dist_link)
    # 创建新的软链接指向新部署的目录：
    run('ln -s %s %s' % (remote_dist_dir, remote_dist_link))
    run('chown -R www-data:www-data %s' % remote_dist_link)
    # 重启fastcgi：
    fcgi = '/etc/init.d/py-fastcgi'
    with settings(warn_only=True):
        run('%s stop' % fcgi)
    run('%s start' % fcgi)
