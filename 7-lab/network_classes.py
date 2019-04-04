class A:
    NID_bits = 8
    HID_bits = 24
    networks = 2 ** NID_bits
    hosts = 2 ** HID_bits

    def __str__(self):
        return 'A'


class B:
    NID_bits = 16
    HID_bits = 16
    networks = 2 ** NID_bits
    hosts = 2 ** HID_bits

    def __str__(self):
        return 'B'


class C:
    NID_bits = 24
    HID_bits = 8
    networks = 2 ** NID_bits
    hosts = 2 ** HID_bits

    def __str__(self):
        return 'C'

