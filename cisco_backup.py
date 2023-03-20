#Backup Cisco config
# import modules needed and set up ssh connection parameters
import paramiko
import datetime
from getpass import getpass

username = input('Enter your usernmae:')
password = getpass()

port = 22
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# define variables
time_now = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
infilepath = "/home/a_avoonna/device_list/"
outfilepath = "/home/a_avoonna/backup/"
devicelist = "chg155077_device_list"

# open device file
input_file = open(infilepath + devicelist, "r")
iplist = input_file.readlines()
input_file.close()

# loop through device list and execute commands
for ip in iplist:
    print('Connecting to device ' + ip)
    ipaddr = ip.strip()
    ssh.connect(hostname=ipaddr, username=username, password=password, port=port)
    stdin, stdout, stderr = ssh.exec_command('show run')
    list = stdout.readlines()
    outfile = open(outfilepath + ipaddr + "_" + time_now, "w")
    for char in list:
        outfile.write(char)
    ssh.close()
    outfile.close()
    print('Backup completed  successfully to device ' + ip)
