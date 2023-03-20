import logging
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import SSHException

username = input('Enter your username: ')
password = getpass()

logging.basicConfig(filename='netmiko_global.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

with open('config_file') as f:
        config_list = f.read().splitlines()

with open('device_file') as f:
        cisco_ios_switch_list = f.read().splitlines()

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

        output = net_connect.send_config_set(config_list)
        print (output)
        net_connect.save_config()
        #show = net_connect.send_command('show run | i logging', read_timeout=200)
        #print (show)
net_connect.disconnect()
