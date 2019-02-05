import random
import socket


def xor(a, b):
    result = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')

    return ''.join(result)


def mod2div(divident, divisor):
    pick = len(divisor)

    tmp = divident[0: pick]

    while pick < len(divident):

        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + divident[pick]
        else:
            tmp = xor('0' * pick, tmp) + divident[pick]

        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    checkword = tmp
    return checkword


def decodeData(data, key):
    l_key = len(key)
    appended_data = data + '0' * (l_key - 1)
    remainder = mod2div(appended_data, key)
    return remainder


def manipulate_data(data):
    data = list(data)

    # Ask for #positions
    number_of_positions = int(input('Enter number of positions to change: '))
    print('number_of_positions =', number_of_positions)

    # Don't change the last CRC remainder code bits
    # Choose a random sample of numbers from 0-(max-3)
    positions = random.sample(range(0, len(data) - 3), number_of_positions)
    print('Changes to be done to these positions: ', positions)

    for i in positions:
        if data[i] == '1':
            data[i] = '0'
        else:
            data[i] = '1'

    data = "".join(data)
    return data


s = socket.socket()
print("Socket successfully created")

port = 1234

s.bind(('', port))
print("socket binded to %s" % (port))
s.listen(5)
print("socket is listening")

while True:
    c, addr = s.accept()
    print('Got connection from', addr)

    data = c.recv(1024).decode()
    print(data)

    option = input('Do you want to interpret as wrong data (y/n): ')
    if option == 'y':
        data = manipulate_data(data)
        print('Changed data =', data)
    else:
        print('Well, I assume you don\'t want to change!')

    if not data:
        break

    key = "1001"

    ans = decodeData(data, key)
    print("Remainder after decoding is->" + ans)

    # If remainder is all zeros then no error has occurred
    temp = "0" * (len(key) - 1)
    if ans == temp:
        c.sendall(b"THANK you Data ->" + data.encode() + b" Received No error FOUND")
    else:
        c.sendall(b"Error in data")

    c.close()
