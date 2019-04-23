#!/usr/bin/python3
import socket
import sys
import os
from threading import Thread

msg = '''
   This program is basic implementation of FTP server
   FTP_DIRECTORY = <currentDir>/ftp_data
   Help commands:
        0. help             : To print this Help message
        1. list             : List all files in the FTP server
        2. upload <path>    : Upload the file
        3. download <file>  : Download the file to current directory
'''

HOST = '127.0.0.1'
COMMAND_PORT = 2100
DATA_PORT = 2000
FTP_DIR = os.getcwd() + '/ftp_data'
handshake_msg = 'Thanks for connecting'
username = 'Mohith'
password = '12345'


def verify_handshake_rightful_user(conn):
    print('Before credentials')
    if handshake_msg == conn.recv(1024).decode():
        print('Before username')
        conn.sendall(b'Username: ')
        if username == conn.recv(1024).decode():
            print('Before Password')
            # user is correct ask for password
            conn.sendall(b'Password: ')
            if password == conn.recv(1024).decode():
                print('Connection successful!')
                conn.sendall(b'Connection Successful!')
                return

    # Reject because of wrong Handshake/credentials
    conn.sendall(b'Connection Refused!')
    sys.exit(1)


def create_data_socket(type, file_name):
    # Create server socket on DATA_PORT
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as d:
        d.bind((HOST, DATA_PORT))
        d.listen()
        print('Waiting for the client...')
        conn, addr = d.accept()
        with conn:
            print('Connection by:', addr)

            # Ready file path
            file_path = os.path.join(FTP_DIR, file_name)
            print('new file_path =', file_path)

            if type == 'upload':
                upload(conn, file_path, file_name)
            elif type == 'download':
                download(conn, file_path, file_name)

        print('Data Connection closed!')


def download(conn, file_path, file_name):
    # Send ACK
    conn.sendall(b'download')

    # send file size first
    file_size = os.stat(file_path).st_size  # int(conn.recv(1024).decode())
    conn.send(str(file_size).encode())
    with open(file_path, 'rb') as f:
        received_size = 0
        while file_size > received_size:
            # f.write(conn.recv(1024))
            conn.send(f.read(1024))
            received_size = received_size + 1024

    print('Downloaded {}'.format(file_name))


def upload(conn, file_path, file_name):
    # Send ACK
    conn.sendall(b'upload')

    # receive file size first
    file_size = int(conn.recv(1024).decode())
    with open(file_path, 'wb+') as f:
        received_size = 0
        while file_size > received_size:
            f.write(conn.recv(1024))
            received_size = received_size + 1024

    print('Uploaded {}'.format(file_name))


def handle_cmd(cmd, conn):
    res = None
    params = cmd.split(' ')

    if params[0] == 'help':
        res = msg
        # print(msg)
        conn.sendall(res.encode())
    elif params[0] == 'list':
        # list all the files on the FTP server
        # print(os.getcwd())
        res = str(os.listdir(FTP_DIR))
        conn.sendall(res.encode())

    elif params[0] == 'upload':
        # For data transfer use DATA_PORT
        res = '{}'.format(DATA_PORT)
        print(res)
        conn.sendall(res.encode())
        file_name = os.path.basename(params[1])
        create_data_socket('upload', file_name)

    elif params[0] == 'download':
        # For data transfer use DATA_PORT
        res = '{}'.format(DATA_PORT)
        print(res)
        conn.sendall(res.encode())
        file_name = os.path.basename(params[1])
        create_data_socket('download', file_name)

    else:
        conn.sendall(b'Unknown command!')


def start_new_client(conn, addr):
    with conn:
        is_active = True

        # Send conformation
        conn.sendall(handshake_msg.encode())

        # Verify Handshake and credentials
        verify_handshake_rightful_user(conn)

        # Listen for commands
        while is_active:
            cmd = conn.recv(1024).decode()
            if cmd == 'exit':
                is_active = False
                print('Connection closed by: ', addr)
            handle_cmd(cmd, conn)


def main():
    # Open server socket
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
        s.bind((HOST, COMMAND_PORT))
        s.listen()
        print('Waiting for the client...')

        while True:
            conn, addr = s.accept()
            print('Connection by: ', addr)
            try:
                Thread(target=start_new_client, args=(conn, addr)).start()
            except Exception as e:
                print('New Client is not started', addr)
                print('Error msg :\n', e)


if __name__ == '__main__':
    main()
