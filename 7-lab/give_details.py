#!/usr/bin/python3

import math
import ipaddress
import itertools
from network_classes import A, B, C
from tabulate import tabulate


def calc_subnet_mask(Class, bits_to_fix):
    subnet_mask = ['0'] * 32

    for i in range(Class.NID_bits):
        subnet_mask[i] = '1'

    for j in range(bits_to_fix + 1):
        subnet_mask[i + j] = '1'

    return "".join(subnet_mask)


def display_forwarding_table(table):
    headings = ['Index', 'Subnet Address', 'Subnet Mask',
                'Broadcast Address', '#Hosts',
                '1st IP', 'Last IP']
    print(tabulate(table, headings))
    # for i in range(2 ** bits_to_fix):
    #     print(i + 1, end='\t\t\t\t')    # index
    #     print(table[i][0], end='\t\t\t\t')  # Subnet Address
    #     print(table[i][1], end='\t\t')  # Subnet Mask
    #     print(table[i][2], end='\t\t')  # Broadcast Address
    #     print(table[i][3], end='\t\t')  # #hosts/subnet
    #     print(end='\t')
    #     print(table[i][4], end='\t\t')  # 1st IP
    #     print(table[i][5], end='\t\t')  # last IP
    #     print()


def get_general_ip(Class, bits_to_fix):
    ip = [[] for _ in range(2 ** bits_to_fix)]
    if type(Class) is B:
        base = '172.30.'
        comb = list(itertools.product(['0', '1'], repeat=bits_to_fix))
        comb = [''.join(list(e)) for e in comb]
        comb = [num + (8 - bits_to_fix) * '0' for num in comb]
        comb = [int(c, 2) for c in comb]
        print(comb)
        subnets_with_nid = [base + str(i) + '.0' for i in comb]
        ip = [base + str(i) + '.0/' + nid_bits for i in comb]
        ip = [ipaddress.ip_network(i) for i in ip]
        # print(ip)

    return ip, subnets_with_nid


def create_table(ip_network, subnets_with_nid):
    table = [[] for _ in range(len(ip_network))]
    for i in range(len(ip_network)):
        table[i].append(i + 1)
        table[i].append(subnets_with_nid[i])  # subnet Address
        table[i].append(subnet_mask_ip)  # Subnet Mask
        l = []  # To hold all ips of a network
        for add in ip_network[i].hosts():
            # print(add)
            l.append(add)

        table[i].append(ip_network[i].broadcast_address)  # Broadcast address
        table[i].append(len(l))  # #hosts per subnet
        table[i].append(l[1])  # First ip
        table[i].append(l[len(l) - 2])  # Last ip

    return table


if __name__ == '__main__':
    networks = 16  # int(input('Enter number of Networks: '))
    hosts = 4094  # int(input('Enter number of Hosts/Ntwk: '))

    print(networks, hosts)

    # find the class based on the #hosts
    # Don't consider the NID and BID
    if hosts <= 2 ** 8 - 2:
        Class = C()
    elif hosts <= 2 ** 16 - 2:
        Class = B()
    elif hosts <= 2 ** 24 - 2:
        Class = A()

    print('Class :', Class)

    # Calculate the #of subnets
    bits_to_fix = math.ceil(math.log(networks, 2))
    print('No.of subents =', bits_to_fix)

    # Calculate the subnet mask
    subnet_mask = calc_subnet_mask(Class, bits_to_fix)
    print('subnet_mask =', subnet_mask)

    subnet_mask_ip = ipaddress.IPv4Address(int(subnet_mask, 2))
    print(subnet_mask_ip)

    nid_bits = str(subnet_mask.count('1'))

    ip_network, subnets_with_nid = get_general_ip(Class, bits_to_fix)
    print(ip_network)
    print(subnets_with_nid)

    table = create_table(ip_network, subnets_with_nid)

    display_forwarding_table(table)
