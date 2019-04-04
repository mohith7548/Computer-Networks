#!/usr/bin/python3

import sys
import time
import socket

# server's address and port-number
HOST = sys.argv[1]
PORT = int(sys.argv[2])
SIZE = 1500
i = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))

        # receive RECEIVE_INTERVAL from server
        RECEIVE_INTERVAL = int(s.recv(1024).decode())   # bytes->str->int
        print('RECEIVE_INTERVAL:', RECEIVE_INTERVAL)

        while True:
            i = i + 1
            print('Waiting till timeout! -', i)
            time.sleep(RECEIVE_INTERVAL)
            # receive data now
            data = s.recv(SIZE)
            if data != b'':
                print('Received Data:', data[:10], '...')
            else:
                print('Server didn\'t send anything!!')


    except Exception as e:
        print('Error:\n', str(e))

