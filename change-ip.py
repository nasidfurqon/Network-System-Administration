import paramiko

HOST = "server"
NAME = "server"
PORT = 22
PASSWORD = "Skills39"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, port=PORT, username=NAME,password=PASSWORD)
command = """
sudo touch /etc/netplan/01-netcfg.yaml;
sudo chmod 777 /etc/netplan/01-netcfg.yaml;
echo 'network:' > /etc/netplan/01-netcfg.yaml;
echo '  version: 2' >> /etc/netplan/01-netcfg.yaml;
echo '  ethernets:' >> /etc/netplan/01-netcfg.yaml;
echo '    ens37:' >> /etc/netplan/01-netcfg.yaml;
echo '      dhcp4: no' >> /etc/netplan/01-netcfg.yaml;
echo '      addresses:' >> /etc/netplan/01-netcfg.yaml;
echo '         - 192.168.10.10/24' >>/etc/netplan/01-netcfg.yaml;
echo '      gateway4: 192.168.10.1' >> /etc/netplan/01-netcfg.yaml;
sudo netplan apply;
"""
stdin, stdout, stderr = client.exec_command(command)

print(stdout.read())
print(stderr.read())
client.close()

