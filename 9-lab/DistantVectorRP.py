#!/usr/bin/python3
# Distant Vector Routing Protocol Program

import os
from node import *


data_path = 'data/sample'
DATA_FILES = os.listdir(os.getcwd() + '/' +  data_path)
all_nodes = ['A', 'B', 'C', 'D']
name_to_node = {}
node_to_number = {}
number_to_node = {}
# Input is the .dat files in the data/ folder


def get_nodes_list():
    global name_to_node, node_to_number
    nodes = []
    for counter, file_name in enumerate(DATA_FILES):
        print('reading', file_name + ' ...')
        with open(data_path + '/' +file_name) as f:
            dist_vector = []
            connected_nodes = []
            name = f.readline().strip()
            line = f.readline()
            while line:
                chars = line.strip().split(' ')
                # print(chars)
                dict = {}
                connected_nodes.append(chars[0])
                dict['destination'] = chars[0]
                dict['cost'] = int(chars[1])
                dict['nexthop'] = chars[0]
                dist_vector.append(dict)
                # print(dist_vector)
                line = f.readline()

            # print('Connected Nodes:', connected_nodes)
            non_connected_nodes = [x for x in all_nodes if x not in connected_nodes]
            for n in non_connected_nodes:
                dict = {}
                dict['destination'] = n
                dict['cost'] = MAX
                dict['nexthop'] = None
                dist_vector.append(dict)

            connected_nodes.remove(name)
            # Sort the list of dits based on the destination like A, B, C, D
            dist_vector = sorted(dist_vector, key=lambda k: k['destination'])
            new_node = Node(name, connected_nodes, dist_vector)
            nodes.append(new_node)
            name_to_node[new_node.name] = new_node
            node_to_number[new_node.name] = counter+1
            number_to_node[counter+1] = new_node.name
            print(new_node)


    print('name_to_node =', name_to_node)
    print('node_to_number =', node_to_number)
    return nodes


def get_min_path(i, node):
    cost = MAX
    for neighbour_name in node.connected_nodes:
        # print('neighbour_name =', neighbour_name)
        neighbour = name_to_node[neighbour_name]
        # cur_cost = (cost to go to the neighbour) + (cost from neighbour to actual destination)
        cur_cost = node.old_vector[node_to_number[neighbour_name]-1]['cost'] + neighbour.old_vector[i]['cost']
        # print('{} + {}'.format(node.old_vector[node_to_number[neighbour_name]-1]['cost'], neighbour.old_vector[i]['cost']))
        if cur_cost < cost:
            cost = cur_cost
            nexthop = neighbour_name

    return cost, nexthop


if __name__ == '__main__':
    # Build Nodes
    nodes = get_nodes_list()

    # Shortest path b/w any two nodes will never contain more than (n-1) edges, where n = #nodes
    # Already when we compute the dist_vector direclty from the data files, we completed one step, so run loop n-2 times now!
    for c in range(len(nodes) -2):
        print('``````````````````Iteration-{}````````````````'.format(c + 1))
        for node in nodes:
            print('for node -', node.name)
            for i in range(len(node.old_vector)):
                dict = {}
                if node.name == number_to_node[i+1]:
                    dict['destination'] = node.name
                    dict['cost'] = 0
                    dict['nexthop'] = node.name
                else:
                    cost, nexthop = get_min_path(i, node)
                    dict['destination'] = number_to_node[i+1]
                    dict['cost'] = cost
                    dict['nexthop'] = nexthop

                node.new_vector.append(dict)

            print('{}-Iteration : Table at {}'.format(c + 1, node.name))
            node.printDVR()

        # Edit each node's new_vector and make it as old_vector and empty new_vector for next iteration, but original data dist_vector is unchanged, see Node class for more details
        for node in nodes:
            node.old_vector = node.new_vector.copy()
            node.new_vector = []
