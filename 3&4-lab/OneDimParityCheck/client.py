import socket
import pickle
import random

HOST = '127.0.0.1'
PORT = 2002


def decode_data(data):
    for i, d in enumerate(data):
        data[i] = data[i][:-1]
        data[i] = chr(int(data[i], 2))
    data = ''.join(data)
    print('Final String is:', data)


def check_row_parity(data):
    for i in range(len(data) - 1):
        s = data[i][:-1]
        # print(s)
        c = s.count('1')
        if c % 2 == 0:
            parity = 0
        else:
            parity = 1
        print(data[i][-1], parity)
        if int(parity) != int(data[i][-1]):
            print('RFalse')
            return False

    print('RTrue')
    return True


def manipulate_data(data):
    # Store the changed data separately and replace at last.
    changed_data = []

    # Ask for #positions
    number_of_positions = int(input('Enter number of positions to change: '))
    print('number_of_positions =', number_of_positions)

    # Choose a random sample of numbers from 0-6
    # Don't change last 7th index bit. Since to verify parity!
    positions = random.sample(range(0, 7), number_of_positions)
    print('Changes to be done to these positions: ', positions)

    # Don't change the parity bits!!!
    # Iterate through each bin string and replace the positions
    for b in data:
        a = list(b)
        for i in positions:
            # print('before:', a)
            if a[i] == '1':
                a[i] = '0'
            else:
                a[i] = '1'
            # print('after:', a)
        changed_data.append("".join(a))

    return changed_data


# data = ['11010001', '11011000', '11011110', '11011110']
# print(check_row_parity(data))
# decode_data(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024)
    final_data = pickle.loads(data)
    print('final_data =', final_data)
    print('Received Data from server!')
    option = input('Do you want to interpret as wrong data (y/n): ')
    if option == 'y':
        final_data = manipulate_data(final_data)
        print('Changed data =', final_data)
    else:
        print('Well, I assume you don\'t want to change!')
    if check_row_parity(final_data):
        print("Data is Safe!")
        decode_data(final_data)
    else:
        print("Data is corrupted!")
# print('Received', repr(data))
