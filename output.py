import subprocess
from subprocess import PIPE
from datetime import datetime

class NiceLogger:
    def log(self, message):
        datenow = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
        print("{0} |  {1}".format(datenow, message))


class DockerHelper:
    niceLogger = NiceLogger()

    def create_network(self):
        command = ["docker", "network", "create", config["NetworkName"]]
        self.run_command(command)

    def pull_container_image(self, containerImage):
        command = ["docker", "pull", containerImage]
        self.run_command(command)
        self.niceLogger.log(" - Pulled " + containerImage)

    def run_container(self, containerName, containerImage, args):
        command = ["docker", "run", "-d", "--net", config["NetworkName"], "--name", containerName]
        command.extend(args)
        command.append(containerImage)

        popen = self.run_command(command)

        error = popen.stderr.readline().decode("utf-8")

        if error != "":
            error = error.replace("\n", "")
            self.niceLogger.log("An error occurred:" + error)
        else:
            id = popen.stdout.readline().decode("utf-8")
            id = id.replace("\n", "")
            self.niceLogger.log(" - New container ID " + id)

    def run_container_with_exec(self, containerName, containerImage, execCommand, args):
        command = ["docker", "run", "-d", "--net", config["NetworkName"], "--name", containerName]
        command.extend(args)
        command.append(containerImage)
        command.append(execCommand)

        self.run_command(command)

    def run_command(self, command):
        debugcommand = " - {0}".format(" ".join(command))
        self.niceLogger.log(debugcommand)

        popen = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        popen.wait(500) # wait a little for docker to complete

        return popen


# Some questions
containerNameSuffix = ""
gethost = input("Local mode [Y/n]?")
if gethost == "":
    containerNameSuffix = "-local"

registry = ""

# Config
config = {
    "NetworkName": "NginxNetwork",
    "PapertrailUrl": "top-secret-url",
    "DataDogApiKey": "TOPSECRET-KEY"
}

containerImages = {
    "Datadog": "datadog/docker-dd-agent:latest",
    "Papertrail": "gliderlabs/logspout",
    "SecretProject1": registry + "SecretProject1:latest",
    "Nginx": registry + "nginx-custom:latest",
    "SecretProject2": registry + "SecretProject2:latest",
}

containerNames = {
    "Datadog": "datadog" + containerNameSuffix,
    "Papertrail": "papertrail" + containerNameSuffix,
    "SecretProject1": "SecretProject1" + containerNameSuffix,
    "Nginx": "nginx" + containerNameSuffix,
    "SecretProject2": "SecretProject2" + containerNameSuffix,
}

niceLogger = NiceLogger()
niceLogger.log("Variables:")
niceLogger.log("Container name suffix: " + containerNameSuffix)
niceLogger.log("Registry prefix: " + registry)
niceLogger.log("")

niceLogger.log("Cleaning images with <none> tags.")

dockerHelper = DockerHelper()

niceLogger.log("Pulling new images.")
dockerHelper.pull_container_image(containerImages["Datadog"])
dockerHelper.pull_container_image(containerImages["Papertrail"])
dockerHelper.pull_container_image(containerImages["SecretProject1"])
dockerHelper.pull_container_image(containerImages["Nginx"])
dockerHelper.pull_container_image(containerImages["SecretProject2"])

niceLogger.log("Creating {0} network.".format(config["NetworkName"]))
dockerHelper.create_network()

niceLogger.log("Adding SecretProject2.")
dockerHelper.run_container(containerNames["SecretProject2"], containerImages["SecretProject2"],
                           ["--env-file", "SecretProject2-env.list"])

# Add papertrail/datadog logging to DigitalOcean only
if containerNameSuffix == "":
    niceLogger.log("Adding datadog.")
    dataDogArgs = ["-v", "/var/run/docker.sock:/var/run/docker.sock:ro",
                   "-v", "/proc/:/host/proc/:ro",
                   "-v", "/sys/fs/cgroup/:/host/sys/fs/cgroup:ro",
                   "-e", "API_KEY=" + config["DataDogApiKey"]
                   ]
    dockerHelper.run_container(containerNames["Datadog"], containerImages["Datadog"], dataDogArgs)

    niceLogger.log("Adding papertrail.")
    paperTrailArgs = ["-e", 'SYSLOG_HOSTNAME="{{.ContainerName}}"',
                      "--restart=always",
                      "-v", "/var/run/docker.sock:/var/run/docker.sock"
                      ]
    papertTrailExec = "syslog://" + config["PapertrailUrl"]
    dockerHelper.run_container_with_exec(containerNames["Papertrail"], containerImages["Papertrail"], papertTrailExec,
                                         paperTrailArgs)
else:
    niceLogger.log("Skipping datadog and papertrail for local mode.")

niceLogger.log("Adding SecretProject1.")
dockerHelper.run_container(containerNames["SecretProject1"], containerImages["SecretProject1"],
                           ["--expose", "5000", "--env-file", "SecretProject1-env.list"])

niceLogger.log("Adding Nginx.")
nginxArgs = ["-p", "80:80",
             "-p", "443:443",
             "--link", containerNames["SecretProject1"] + ":SecretProject1"
             ]
dockerHelper.run_container(containerNames["Nginx"], containerImages["Nginx"], nginxArgs)