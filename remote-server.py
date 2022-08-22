import paramiko

HOST = "server"
NAME = "server"
PORT = 22
PASSWORD = "Skills39"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=NAME,password=PASSWORD)
sftp = client.open_sftp()
sftp.put("image_cleaner.sh", "/home/yang/images/image_cleaner.sh")
stdin, stdout, stderr = client.exec_command("sudo su")
stdin.write('\n')

command = "cd /home/yang/images/;chmod -R 777 image_cleaner.sh;./image_cleaner.sh;"
stdin, stdout, stderr = client.exec_command(command)

print(stdout.read())
print(stderr.read())
client.close()

