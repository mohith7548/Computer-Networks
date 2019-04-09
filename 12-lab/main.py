#!/usr/bin/python3

import multiprocessing
import time
import random
from Packet import *

intro = '''
A, B, C are arranged in clockwise cyclic order
SrcID for A = 10, B = 20, C = 30
Packets colors: Red(0), Blue(1), Green(2)
'''

p = []
q = []
index_name_map = {0: 'A', 1: 'B', 2: 'C'}
id_name_map = {10: 'A', 20: 'B', 30: 'C'}
name_index_map = {'A': 0, 'B': 1, 'C': 2}
id_ip_map = {10: '1.1.1.1', 20: '2.2.2.2', 30: '3.3.3.3'}


def red_fun(name, id, obj):
    # Decrement ttl
    new_ttl = int(obj.ttl, 2) - 1
    # Two new green packets are generated with the decremented TTL, but with the
    # same source ID X, and seq. num Y
    green_packet1 = Packet(srcID=int(obj.srcID, 2), seq_number=int(obj.seq_number, 2),
                           color=2, ttl=new_ttl, srcIP=id_ip_map[id])
    green_packet2 = Packet(srcID=int(obj.srcID, 2), seq_number=int(obj.seq_number, 2),
                           color=2, ttl=new_ttl, srcIP=id_ip_map[id])

    # P1 send clockwise
    q[(name_index_map[name] + 1) % 3].put(green_packet1)
    # P2 send anti-clockwise
    q[(name_index_map[name] - 1) % 3].put(green_packet2)


def get_direction(cur_id, src_id):
    #       A        ___       (10)
    #    C      B          (30)     (20)
    if cur_id > src_id:
        return 0  # Clockwise
    else:
        return 1  # Anti-Clockwise


def green_fun(name, id, obj):
    new_ttl = int(obj.ttl, 2)
    if random.randint(0, 1) == 1:
        # Decrement ttl
        new_ttl = new_ttl - 1
    if new_ttl > 0:
        # send the green packet onwards (with the same source
        # ID field X, and seq. num Y) in the same cyclical direction in which it was
        # received
        green_packet = Packet(srcID=int(obj.srcID, 2), seq_number=int(obj.seq_number, 2),
                              color=2, ttl=new_ttl, srcIP=id_ip_map[id])
        if get_direction(id, int(obj.srcID, 2)) == 0:
            q[(name_index_map[name] + 1) % 3].put(green_packet)
        else:
            q[(name_index_map[name] - 1) % 3].put(green_packet)

    elif new_ttl == 0:
        # generate a blue packet with the same source ID field X, and
        # send the blue packet along the same cyclical direction
        blue_packet = Packet(srcID=int(obj.srcID, 2), seq_number=int(obj.seq_number, 2),
                             color=1, ttl=new_ttl, srcIP=id_ip_map[id])
        # send the blue packet along the same cyclical direction
        if get_direction(id, int(obj.srcID, 2)) == 0:  # Clockwise
            q[(name_index_map[name] + 1) % 3].put(blue_packet)
        else:  # Anti-Clockwise
            q[(name_index_map[name] - 1) % 3].put(blue_packet)


def blue_fun(name, id, obj):
    msg = '''
    Packet Format:
    srcID:      {}  {}
    seq_number: {}  {}
    ip_address: {}
    '''.format(obj.srcID, int(obj.srcID, 2),
               obj.seq_number, int(obj.seq_number, 2),
               obj.srcIP
               )
    print('{}: {}'.format(name, msg))


def send_new_packet_every_time(name, id):
    # Used by All processes
    packet_number = 0
    while True:
        packet_number = packet_number + 1
        print('{}: Generating new Packet-{}'.format(name, packet_number))
        packet = Packet(srcID=id, color=0, ttl=8, seq_number=1, srcIP=id_ip_map[id])
        # Send in random direction by default
        rand_id = random.randint(1, 3) * 10
        q[name_index_map[id_name_map[rand_id]]].put(packet)
        print('{}: Message sent to {}'.format(name, id_name_map[rand_id]))
        time.sleep(5)


def node(name, id, msg_queue):
    # Demon sub-process that sends new packet for every 5 sec in random clock direction
    multiprocessing.Process(target=send_new_packet_every_time, args=(name, id,)).start()

    # Actual process
    while True:
        # print('{}: I\'m Alive'.format(name))
        if not msg_queue.empty():
            obj = msg_queue.get()
            if type(obj) is Packet:
                # print('{}: {}\n'.format(name, obj))
                if int(obj.color, 2) == 0:  # Red Packet
                    red_fun(name, id, obj)

                elif int(obj.color, 2) == 1:  # Green Packet
                    green_fun(name, id, obj)

                elif int(obj.color, 2) == 2:  # Blue Packet
                    blue_fun(name, id, obj)

        # time.sleep(4)


if __name__ == '__main__':
    print(intro)
    # manager = multiprocessing.Manager()
    for i in range(3):
        queue = multiprocessing.Queue()
        # print((i + 1) * 10)
        process = multiprocessing.Process(target=node, args=(index_name_map[i], (i + 1) * 10, queue))
        p.append(process)
        q.append(queue)

    for process in p:
        process.start()
