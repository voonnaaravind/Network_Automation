import logging
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import SSHException

import re



username = input('Enter your username: ')
password = getpass()

logging.basicConfig(filename='netmiko_global.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

#validation = '/home/a_avoonna/validation/'

#with open('chg155077_config_file') as f:
#       config_list = f.read().splitlines()

with open('device_file') as f:
        cisco_ios_switch_list = f.read().splitlines()

devices = []

#clearing the old data from the CSV file and writing the headers
f = open("ios.csv", "w+")
f.write("IP Address, Hostname, Current_Version, Current_Image, Serial_Number, Device_Model")
f.write("\n")
f.close()


for switch in cisco_ios_switch_list:
        print ('Connecting to device" ' + switch)
        ip_address_of_devices = switch
        ios_device = {
                'device_type': 'cisco_ios',
                'ip': ip_address_of_devices,
                'username': username,
                'password': password
        }

        try:
                net_connect = ConnectHandler(**ios_device)
        except (AuthenticationException):
                print ('Authentication failure: ' + ip_address_of_devices)
                continue
        except (NetMikoTimeoutException):
                print ('Timeout to device: ' + ip_address_of_devices)
                continue
        except (EOFError):
                print('End of file while attempting device ' + ip_address_of_devices)
                continue
        except (SSHException):
                print ('SSH Issue ' + ip_address_of_devices)
                continue
        except Exception as unknow_error:
                print('Some other error: ' + str(unknow_error))
                continue

        #net_connect.save_config()
        #show = net_connect.send_command('show run | i logging', read_timeout=200)
        #print (show)
        sh_ver_output = net_connect.send_command('show version')
        #print(sh_ver_output)
        regex_version = re.compile(r'Cisco\sIOS\sSoftware.+Version\s([^,]+)')
        version = regex_version.findall(sh_ver_output)
        regex_hostname = re.compile(r'(\S+)\suptime')
        hostname = regex_hostname.findall(sh_ver_output)
        regex_serial = re.compile(r'Processor\sboard\sID\s(\S+)')
        serial = regex_serial.findall(sh_ver_output)
        regex_ios = re.compile(r'System\simage\sfile\sis\s"([^ "]+)')
        ios = regex_ios.findall(sh_ver_output)
        regex_model = re.compile(r'[Cc]isco\s(\S+).*memory.')
        model = regex_model.findall(sh_ver_output)
        devices.append([ip_address_of_devices,hostname[0],version[0],ios[0],serial[0],model[0]])
        #print(devices)

net_connect.disconnect()

for i in devices:
    i = ", ".join(i)
    f = open("ios.csv", "a+", newline="")
    f.write(i)
    f.write("\n")
    f.close()


