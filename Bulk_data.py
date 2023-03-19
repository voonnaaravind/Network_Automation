import re
from getpass import getpass
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException
from netmiko.exceptions import AuthenticationException
from netmiko.exceptions import SSHException


username = input('Enter your username: ')
password = getpass()


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
        #list where informations will be stored
        devices = []


        #clearing the old data from the CSV file and writing the headers
        f = open("IOS.csv", "w+")
        f.write("IP Address, Hostname, Uptime, Current_Version, Current_Image, Serial_Number, Device_Model, Device_Memory")
        f.write("\n")
        f.close()

  # execute show version on router and save output to output object

sh_ver_output = net_connect.send_command('show version')

  #finding hostname in output using regular expressions

regex_hostname = re.compile(r'(\S+)\suptime')
hostname = regex_hostname.findall(sh_ver_output)

  #finding uptime in output using regular expressions

regex_uptime = re.compile(r'\S+\suptime\sis\s(.+)')
uptime = regex_uptime.findall(sh_ver_output)
uptime = str(uptime).replace(',' ,'').replace("'" ,"")
uptime = str(uptime)[1:-1]


  #finding version in output using regular expressions

regex_version = re.compile(r'Cisco\sIOS\sSoftware.+Version\s([^,]+)')
version = regex_version.findall(sh_ver_output)
  #finding serial in output using regular expressions

regex_serial = re.compile(r'Processor\sboard\sID\s(\S+)')
serial = regex_serial.findall(sh_ver_output)
  #finding ios image in output using regular expressions

regex_ios = re.compile(r'System\simage\sfile\sis\s"([^ "]+)')
ios = regex_ios.findall(sh_ver_output)
  #finding model in output using regular expressions

regex_model = re.compile(r'[Cc]isco\s(\S+).*memory.')
model = regex_model.findall(sh_ver_output)

  #finding the router's memory using regular expressions

regex_memory = re.search(r'with (.*?) bytes of memory', sh_ver_output).group(1)
memory = regex_memory

  #append results to table [hostname,uptime,version,serial,ios,model]

devices.append([ip_address_of_devices, hostname[0],uptime,version[0],ios[0], serial[0],model[0], memory])

  #print all results (for all routers) on screen

for i in devices:
    i = ", ".join(i)
    f = open("IOS.csv", "a")
    f.write(i)
    f.write("\n")
    f.close()
