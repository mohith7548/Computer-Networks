#!/usr/bin/python3

import re
import subprocess
from subprocess import Popen, PIPE

IP = input('Enter the ip address: ')

# Do ping scan so as to update the local ARP cache.
pid = Popen(['ping', '-c 2', IP], stdout=PIPE)
res = pid.communicate()
#print(res)

# Now the arp has the mac add of the ip add
# jUst ask arp command to fetch the required ip's mac
pid = Popen(['arp', '-n', IP], stdout=PIPE)
res = pid.communicate()[0].decode()
print(res)

# Use Regular expression to cut-out the macid from the output
mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", res).group(0)
print('MacAddress:', mac)

