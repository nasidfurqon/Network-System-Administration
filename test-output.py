from datetime import datetime
from distutils.cmd import Command
import paramiko
import subprocess
from subprocess import PIPE
from datetime import datetime

class NiceLogger:
    def log(self, message):
        datenow = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
        print("{0} |  {1}".format(datenow, message))

HOST = "server"
NAME = "server"
PORT = 22
PASSWORD = "Skills39"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=NAME,password=PASSWORD)

class DockerHelper:
    niceLogger = NiceLogger()
    
    def pull_container_image(self):
        command = "sudo docker pull python:3.8-slim"
        stdin, stdout, stderr = client.exec_command(command)
        print(stdout.read())
        print(stderr.read())
        self.niceLogger.log(" - Pulled python")

niceLogger = NiceLogger()
dockerHelper = DockerHelper()

niceLogger.log("pulling new container")
dockerHelper.pull_container_image()
client.close()
