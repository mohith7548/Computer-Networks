#!/usr/bin/python3

import socket


inputString = input('Enter the Hostname: ')
ipAdd = socket.gethostbyname(inputString)
print(inputString + 'is at:', ipAdd)
