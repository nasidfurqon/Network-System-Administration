from distutils.cmd import Command
import paramiko
import subprocess
from subprocess import PIPE
from datetime import datetime

HOST = "server"
NAME = "server"
PORT = 22
PASSWORD = "Skills39"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=NAME,password=PASSWORD)

class DockerHelper:
    def pull_container_image(self):
        command = "sudo docker pull nginx"
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read())
        print(stderr.read())
    def run_container(self):
        command = "sudo docker run -d -p 8080:80 --name webserver nginx:latest"
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read())    
        print(stderr.read())
   
command = "sudo apt-get install docker.io -y"
stdin, stdout, stderr = client.exec_command(command)
print(stdout.read())
print(stderr.read())

dockerHelper = DockerHelper()
dockerHelper.pull_container_image()

dockerHelper.run_container()
client.close()
