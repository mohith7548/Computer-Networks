import socket

HOST = '127.0.0.1'
PORT = 2003
parity_bit_indexes = [1, 2, 4, 8, 16, 32]


def cal_redundant_bits():
    r = 0
    m = number_of_data_bits
    while 2 ** r < m + r + 1:
        r = r + 1

    return r


def get_redundant_bits_indexes():
    red_list = []
    # TODO: Generate them automatically
    red_list.append([1, 3, 5, 7])
    red_list.append([2, 3, 6, 7])
    red_list.append([4, 5, 6, 7])
    # for i in range(number_of_redundant_bits):
    #     a = []
    #     j = i
    #     while len(a) <= total_bits:
    #         a.append(2**j + j)
    #         j = j + 1
    return red_list


def arrange():
    final_bits = ['-1'] * total_bits
    print(final_bits)
    c = 0
    for i in range(len(final_bits)):
        if i + 1 not in parity_bit_indexes:
            final_bits[i] = data_bits[c]
            c = c + 1

    print(final_bits)
    return final_bits


def cal_and_put_parity_bits():
    for i in range(len(red_bits_indexes_list)):
        # print('i =', i)
        st = ''
        for j in range(len(red_bits_indexes_list[i])):
            # print('j =', j)
            if j == 0:
                continue
            st = st + final_bits[red_bits_indexes_list[i][j] - 1]
        print(st)
        c = st.count('1')
        if c % 2 == 0:
            final_bits[red_bits_indexes_list[i][0] - 1] = '0'
        else:
            final_bits[red_bits_indexes_list[i][0] - 1] = '1'

    print('final_bits =', final_bits)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print('Waiting for client...')
    conn, addr = s.accept()
    with conn:
        print('Connection by', addr)

        data_bits = '1101'  # input('Enter data bits: ')
        number_of_data_bits = len(data_bits)
        data_bits = list(data_bits)  # Converting to a list of character bytes
        number_of_redundant_bits = cal_redundant_bits()
        total_bits = number_of_data_bits + number_of_redundant_bits
        final_bits = arrange()
        print('number_of_redundant_bits:', number_of_redundant_bits)
        red_bits_indexes_list = get_redundant_bits_indexes()
        print('red_bits_indexes_list:', red_bits_indexes_list)
        cal_and_put_parity_bits()
        conn.sendall(''.join(final_bits).encode())
        print('Sending data..')

print('Data sent')
