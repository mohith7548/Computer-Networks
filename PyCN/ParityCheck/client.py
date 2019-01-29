import socket
import pickle

HOST = '127.0.0.1'
PORT = 2001


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


# data = ['11010001', '11011000', '11011110', '11011110', '00001001']
# print(check_row_parity(data) and check_col_parity(data))
# decode_data(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024)
    final_data = pickle.loads(data)
    print(final_data)
    if check_row_parity(final_data) and check_col_parity(final_data):
        print("Data is Safe!")
        decode_data(final_data)
    else:
        print("Data is corrupted!")
# print('Received', repr(data))
