#!/usr/bin/env python

#autor:glacier
#2015-6-20

from fabric.api import settings, cd,  run, env, prompt, sudo, hide, show, prefix, get, local, open_shell, put,reboot,parallel,roles


def remote_server():
    env.hosts = ['x.x.x.x']
    env.user = 'user'
    #env.sudo_user = 'user'
    env.key_filename = '/root/bicher.pem'
    env.shell = '/bin/sh'
    #env.roledefs = {
            #'testserver': ['x.x.x.x']  
            # }

def task():
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),  warn_only=True):
        sudo('cat show_cpuinfo.py')

#
def task1():
    with settings(hide('everything'), warn_only=True):
        run('ls -l')

def task2():
    with prefix('source /etc/profile'):
        sudo('sh /root/who.sh')

def task3():
    get('show_cpuinfo.py')

def task4():
    local('ls')

def task5():
    open_shell('cat show_cpuinfo.py')

def task6():
    prompt('enter your name:')

def task7():
    put('fabfile.py')

def task8():
    reboot('5')

@parallel(5)
def task9():
    sudo('sh /root/who.sh')

#@roles('testserver')
#def task10():
#    sudo('sh /root/who.sh') 

def add_arg(name):
    print 'your name %s' %name

def ex_sh(file):
    #with cd('/root/user'):
     run(file)
