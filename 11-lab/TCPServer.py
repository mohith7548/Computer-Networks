import os
import time
import socket

HOST = '127.0.0.1'
PORT = 3000
SIZE = 1500
SEND_INTERVAL = 5 # seconds
i = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.bind((HOST, PORT))
        print('Listening for the client...')
        s.listen()
        conn, addr = s.accept()
        print('Connection accepted!')
        # print('connection:', conn)
        print('Client IP, Port:', addr)

        with conn:
            # send the SEND_INTERVAL to client
            conn.sendall(str(SEND_INTERVAL).encode())   # int->str->bytes

            # send 1500 bytes of data for every SEND_INTERVAL time
            while True:
                i = i + 1
                print('Waiting till timeout! -', i)
                time.sleep(SEND_INTERVAL)
                # send data now
                data = os.urandom(SIZE) # Already in bytes
                print('data =', data[:10], '...')
                print('sending...')
                conn.sendall(data)
                print('sent!')


    except Exception as e:
        print('Error:\n', str(e))