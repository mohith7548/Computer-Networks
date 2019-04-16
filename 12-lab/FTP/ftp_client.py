#!/usr/bin/python3
import socket
import getpass
import sys
import os

HOST = '172.30.3.202'
COMMAND_PORT = 2100
DATA_PORT = 2000


def handle_handshake_auth(s):
    # Regular Handshake
    msg = s.recv(1024)
    print('Server:', msg.decode())
    s.sendall(msg)

    # Send credentials
    # username
    username = input(s.recv(1024).decode())
    s.sendall(username.encode())
    # Password
    password = getpass.getpass(s.recv(1024).decode())
    s.sendall(password.encode())

    # Get status message
    msg = s.recv(1024).decode()
    print(msg)
    if msg == 'Connection Successful!':
        return
    else:
        sys.exit(1)


def start_data_socket(file_path, port):
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as d:
        d.connect((HOST, port))
        print('Data Channel socket connection successful')

        print('file_path: {}\n'.format(file_path))
        # Get file from the file_path => convert to binary and transfer

        # Receive ACK
        ack = d.recv(1024).decode()
        if ack == 'upload':
            print('Start upload')
            # send file size first
            file_size = os.stat(file_path).st_size  # in bytes
            d.send(str(file_size).encode())
            # Now send actual data
            with open(file_path, 'rb') as f:
                sent_size = 0
                while file_size >= sent_size:
                    d.send(f.read(1024))
                    sent_size = sent_size + 1024

            print('Uploaded {}'.format(file_path))

        elif ack == 'download':
            print('Download started')
            # receive file size first
            file_path = os.path.join(os.getcwd(), file_path)
            file_size = int(d.recv(1024).decode())  # in bytes
            # Now receive actual data
            with open(file_path, 'wb+') as f:
                sent_size = 0
                while file_size >= sent_size:
                    # d.send(f.read(1024))
                    f.write(d.recv(1024))
                    sent_size = sent_size + 1024

            print('Downloaded {}'.format(file_path))

        # Send file
        print('Data Connection closed!')


def main():
    # Open client socket
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        s.connect((HOST, COMMAND_PORT))
        print('Connected to FTP server')

        handle_handshake_auth(s)

        # Communicate with the FTP server
        while True:
            cmd = str(input('-> '))
            params = cmd.split(' ')
            if params[0] == 'exit':
                # Exit after sending 'exit' to server, 'caz it also has to exit
                s.sendall(cmd.encode())
                sys.exit(0)

            s.sendall(cmd.encode())
            # wait for the result
            res = s.recv(1024).decode()
            print('Result: ', res)

            if params[0] == 'upload':
                start_data_socket(params[1], int(res))
            elif params[0] == 'download':
                start_data_socket(params[1], int(res))


if __name__ == '__main__':
    main()
