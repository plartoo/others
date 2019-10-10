import pdb


def reverse_integer2(signed_integer):
    # python implementation
    pass


def reverse_integer1(signed_integer):
    # langauge independent (kind of) implementation
    integers = []
    while signed_integer != 0:
        integers.append(signed_integer % 10)
        signed_integer = int(signed_integer / 10)

    reversed_int = 0
    exponent = len(integers)
    for i, n in enumerate(integers):
        exponent -= 1
        reversed_int += n * (10 ** exponent)
    print(reversed_int)


if __name__ == '__main__':
    reverse_integer1(123)
    reverse_integer1(321)
    reverse_integer1(4800)

