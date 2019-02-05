import socket

HOST = '127.0.0.1'
PORT = 2003

red_bits_indexes_list = [[1, 3, 5, 7], [2, 3, 6, 7], [4, 5, 6, 7]]


def check_input_data():
    for i in range(len(red_bits_indexes_list)):
        # print('i =', i)
        st = ''
        for j in range(len(red_bits_indexes_list[i])):
            st = st + final_bits[red_bits_indexes_list[i][j] - 1]
        print(st)
        c = st.count('1')
        if c % 2 == 1:
            print('Data is corrupted!')
            return
    print('Data is safe')


# final_bits = ['1'f, '0', '1', '0', '1', '0', '1']
# check_input_data()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    final_bits = s.recv(1024)
    final_bits = final_bits.decode()
    print(final_bits)
    check_input_data()
