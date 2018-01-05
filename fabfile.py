#!/usr/bin/env python
from fabric.api import *
from fabric.contrib.files import exists


env.use_ssh_config = False
env.hosts = ["192.168.200.107"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"
env.port = 22

def deploy(folder_to_deploy, remote_foldername="default"):

	branch = local("cd %s && git symbolic-ref HEAD 2>/dev/null" % folder_to_deploy, capture=True)
	branch = branch.split("/")
	branch = branch[2]
	if branch != "* master" and branch != "":

		print ("The branch is not master")
		remote_foldername = branch

	if exists('/var/www/html/%s' % folder_to_deploy, use_sudo=True):
		print ("that's nice")
	else: 
		run("cd /var/www/html && mkdir %s" % folder_to_deploy)

	local("scp -r %s/release/ ubuntu@192.168.200.107:/var/www/html/%s/%s" % (folder_to_deploy, folder_to_deploy, remote_foldername))

	print ("Test the journey here: http://bb.assist.ro/%s/%s" % (folder_to_deploy, remote_foldername))
    