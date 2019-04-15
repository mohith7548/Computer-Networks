import socket

HOST = '127.0.0.1'
PORT = 3000


def get_output(data):
    output = None
    commands = data.split(' ')
    if commands[0] == 'ADD':
        arg1 = int(commands[1])
        arg2 = int(commands[2])
        output = arg1 + arg2

    elif commands[0] == 'SUB':
        arg1 = int(commands[1])
        arg2 = int(commands[2])
        output = arg1 - arg2

    elif commands[0] == 'MUL':
        arg1 = int(commands[1])
        arg2 = int(commands[2])
        output = arg1 * arg2

    elif commands[0] == 'DIV':
        arg1 = int(commands[1])
        arg2 = int(commands[2])
        output = arg1 / arg2

    elif commands[0] == 'MOD':
        arg1 = int(commands[1])
        arg2 = int(commands[2])
        output = arg1 % arg2

    return str(output)


with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print('UDP server up and running!')

    # Waiting for client here

    # Handshake
    data, address = s.recvfrom(1024)
    # print(data)
    print('Response from client\nMessage: {}\nAddress: {}\n'.format(data.decode(), address))
    s.sendto(b'What can I help you with?', address)

    # Server Stub: UnPack the Data
    data, address = s.recvfrom(1024)
    print('Data received from the client\nMessage: {}\nAddress: {}\n'.format(data.decode(), address))

    # Compute
    print('Computing...')
    output = get_output(data.decode())

    # Send back
    print('Sending the result')
    s.sendto(output.encode(), address)
