class Packet:
    # Red - 0; Blue - 1; Green - 2

    def __init__(self, color, ttl, seq_number, srcID, srcIP):
        # self.color = self.color_bit_map[color]
        self.color = '{0:08b}'.format(color)
        self.ttl = '{0:08b}'.format(ttl)
        self.seq_number = '{0:08b}'.format(seq_number)
        self.srcID = '{0:08b}'.format(srcID)
        # This is not shown, update at every node.
        # Extra functionality because of last color function demand
        self.srcIP = srcIP

    def __str__(self):
        return '''
        Packet Format:
        srcID:      {}  {}
        color:      {}  {}
        ttl:        {}  {}
        seq_number: {}  {}
        '''.format(self.srcID, int(self.srcID, 2),
                   self.color, int(self.color, 2),  # self.bit_color_map[self.color],
                   self.ttl, int(self.ttl, 2),
                   self.seq_number, int(self.seq_number, 2),
                   )
