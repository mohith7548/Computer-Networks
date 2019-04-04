MAX = 9999999999999999999999999999999999999999999999999999

class Node(object):
    """docstring for each Node in the given Graph.

        The connected_nodes contains list of all directly connected Nodes
        For example,
        ['X', 'Y', 'Z']

        The dist_vector is the list of dict items.
        For example,
        [
            {'destination': "X", 'cost': 0, 'nexthop': 'Z'},
            {'destination': "Y", 'cost': 1, 'nexthop': 'Y'},
            {'destination': "Z", 'cost': 2, 'nexthop': 'X'},
        ]
    """

    def __init__(self, name, connected_nodes, dist_vector):
        self.name = name
        self.connected_nodes = connected_nodes
        self.dist_vector = dist_vector
        self.old_vector = dist_vector.copy()
        self.new_vector = []


    def printDVR(self):
        msg = 'Dest\t' + 'Cost\t' + 'NextHop\n'
        for item in self.new_vector:
            cost = '∞' if item['cost'] == MAX else item['cost']
            msg = msg + item['destination'] + '\t' + str(cost) + '\t' + str(item['nexthop']) + '\n'

        print(msg)


    def __str__(self):
        msg = 'Name:' + self.name + '\n' + 'Distant Vector Table:\n'
        msg = msg + 'Connected Nodes' + str(self.connected_nodes) + '\n'
        msg = msg + 'Dest\t' + 'Cost\t' + 'NextHop\n'
        for item in self.dist_vector:
            cost = '∞' if item['cost'] == MAX else item['cost']
            msg = msg + item['destination'] + '\t' + str(cost) + '\t' + str(item['nexthop']) + '\n'

        return msg
        
