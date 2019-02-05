import random
import socket

HOST = '127.0.0.1'
PORT = 2003

red_bits_indexes_list = [[1, 3, 5, 7], [2, 3, 6, 7], [4, 5, 6, 7]]


def check_input_data():
    isCorrupted = False
    r1r2r3 = ''
    for i in range(len(red_bits_indexes_list)):
        # print('i =', i)
        st = ''
        for j in range(len(red_bits_indexes_list[i])):
            st = st + final_bits[red_bits_indexes_list[i][j] - 1]
        print(st)
        c = st.count('1')
        r1r2r3 = r1r2r3 + str(c % 2)
        if c % 2 == 1:
            isCorrupted = True
    if not isCorrupted:
        print('Data is safe!')
    else:
        # reverse binary number before converting to decimal
        corrupted_position = int(r1r2r3[::-1], 2)
        print('Data is Corrupted!')
        print('At Position:', corrupted_position)
        print('At Index:', corrupted_position - 1)


def manipulate_data(bits):
    fbits = list(bits)

    # Ask for #positions
    number_of_positions = int(input('Enter number of positions to change: '))
    print('number_of_positions =', number_of_positions)

    # Choose a random sample of numbers from 0-max
    positions = random.sample(range(0, len(bits)), number_of_positions)
    print('Changes to be done to these positions: ', positions)

    for i in positions:
        if fbits[i] == '1':
            fbits[i] = '0'
        else:
            fbits[i] = '1'

    return fbits


# final_bits = ['1', '0', '1', '0', '1', '0', '1']
# print('Received Data from server!')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    final_bits = s.recv(1024)
    final_bits = final_bits.decode()
    print(final_bits)
    print('Received Data from server!')
    option = input('Do you want to interpret as wrong data (y/n): ')
    if option == 'y':
        final_bits = manipulate_data(final_bits)
        print('Changed data =', final_bits)
    else:
        print('Well, I assume you don\'t want to change!')
    check_input_data()
