import socket

HOST = '127.0.0.1'
PORT = 3000
address = (HOST, PORT)

with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:

    # Handshake
    print('sending message...')
    s.sendto(b'Hii I\'m Client!', address)
    print('Receiving message...')
    data = s.recv(1024)
    print('Server says:', data.decode())

    # Assume user wants to do Addition

    # Client Stub: Pack the data and send
    data = 'ADD 2 3'
    print('Packing and sending data to server...')
    s.sendto(data.encode(), address)

    # Wait for the Output
    print('Waiting for the remote server...')
    output = s.recv(1024)
    print('Output: ', output.decode())

