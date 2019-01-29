import socket
import pickle

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


# data = ['11010001', '11011000', '11011110', '11011110']
# print(check_row_parity(data))
# decode_data(data)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = s.recv(1024)
    final_data = pickle.loads(data)
    print(final_data)
    if check_row_parity(final_data):
        print("Data is Safe!")
        decode_data(final_data)
    else:
        print("Data is corrupted!")
# print('Received', repr(data))
