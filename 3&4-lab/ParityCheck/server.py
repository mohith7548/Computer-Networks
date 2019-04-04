import socket
import pickle

# HOST = '127.0.0.1'
HOST = '172.30.1.204'
PORT = 2000
data = 'Kiss me'


def convert_to_bin():
    bin_data = ' '.join(format(ord(x), 'b') for x in data)
    print(bin_data, type(bin_data))
    bin_data = bin_data.split(' ')
    # bin_data = list(map(int, bin_data))
    print(bin_data, type(bin_data))
    return bin_data


def add_row_parity(bin_list):
    for i, bin in enumerate(bin_list):
        c = bin.count('1')
        print(c, '-')
        if c % 2 == 0:
            bin_list[i] = bin + '0'

        else:
            bin_list[i] = bin + '1'

    print(bin_list)
    return bin_list


def add_col_parity(bin_list):
    col_parity = []
    for i in range(len(bin_list[0]) - 1):
        col = ''
        for ar in bin_list:
            col = col + ar[i]
        c = col.count('1')
        if c % 2 == 0:
            col_parity.append('0')

        else:
            col_parity.append('1')

    print(col_parity, type(col_parity))
    finalString = ''
    for string in col_parity:
        finalString = finalString + string
    bin_list.append(finalString)
    return bin_list


# a = convert_to_bin()
# a = add_row_parity(a)
# a = add_col_parity(a)
# print('final: ', a)
print('Our Data is:', data)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connection by', addr)
        # convert to binary
        a = convert_to_bin()
        a = add_row_parity(a)
        a = add_col_parity(a)
        print('final: ', a)
        print('Sending data..')
        final_data = pickle.dumps(a)
        conn.send(final_data)

print('Data sent')
