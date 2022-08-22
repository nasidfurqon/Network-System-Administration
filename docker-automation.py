import subprocess
from subprocess import PIPE
from datetime import datetime

class DockerHelper:
    def pull_container_image(self):
        command = ["docker", "pull", "nginx"]
        self.run_command(command)

    def run_container(self):
        command = ["docker", "run", "-d", "-p", "8080:80", "--name", "webserver", "nginx:latest"]
        self.run_command(command)

    def run_command(self, command):
        debugcommand = " - {0}".format(" ".join(command))

        popen = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        popen.wait(500) # wait a little for docker to complete

        return popen

dockerHelper = DockerHelper()
dockerHelper.pull_container_image()

dockerHelper.run_container()
