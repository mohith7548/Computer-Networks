import random
import socket
import pickle

HOST = '127.0.0.1'
PORT = 2000


def decode_data(data):
    data = data[:-1]
    for i, d in enumerate(data):
        data[i] = data[i][:-1]
        data[i] = chr(int(data[i], 2))
    data = ''.join(data)
    print('Final String is:', data)


def check_row_parity(data):
    for i in range(len(data) - 1):
        s = data[i][:-1]
        print(s)
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


def check_col_parity(rdata):
    data = rdata[:-1]
    col_parity = []
    for i in range(len(data[0]) - 1):
        col = ''
        for ar in data:
            col = col + ar[i]
        c = col.count('1')
        if c % 2 == 0:
            col_parity.append('0')

        else:
            col_parity.append('1')

    # print(col_parity, type(col_parity))
    finalString = ''
    for string in col_parity:
        finalString = finalString + string
    # print(finalString, rdata[-1])
    if int(rdata[-1]) == int(finalString):
        print('CTrue')
        return True
    else:
        print('CFalse')
        return False


def manipulate_data(x):
    print(x)
    # Store the changed data separately and replace at last.
    changed_data = []

    # Ask for #positions
    number_of_positions = int(input('Enter number of positions to change: '))
    print('number_of_positions =', number_of_positions)

    # Should not change the last bit in each string
    # And last bit sequence, since 2D parity!!
    # Choose a random sample of numbers from 0-7
    positions = random.sample(range(0, 7), number_of_positions)
    print('Changes to be done to these positions: ', positions)

    # Iterate through each bin string and replace the positions
    for b in x[:-1]:
        a = list(b)
        # print('before:', a)
        for i in positions:
            if a[i] == '1':
                a[i] = '0'
            else:
                a[i] = '1'
        # print('after:', a)
        changed_data.append("".join(a))

    # Again add last parity sequence
    changed_data.append(x[-1])
    return changed_data


# data = ['11010001', '11011000', '11011110', '11011110', '00001001']
# print(check_row_parity(data) and check_col_parity(data))
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
    if check_row_parity(final_data) and check_col_parity(final_data):
        print("Data is Safe!")
        decode_data(final_data)
    else:
        print("Data is corrupted!")
# print('Received', repr(data))
