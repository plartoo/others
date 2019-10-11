import pdb


def reverse_str1(strg: bytearray):
    len_strg = len(strg)
    iter_limit = int(len_strg/2)
    i = 0
    while i < iter_limit:
        temp = strg[i]
        strg[i] = strg[len_strg-i-1]
        strg[len_strg-i-1] = temp
        i += 1
    print(strg)


def reverse_str2(strg: bytearray):
    len_strg = len(strg) - 1
    i = 0
    while i < len_strg:
        temp = strg[i]
        strg[i] = strg[len_strg]
        strg[len_strg] = temp
        i += 1; len_strg -= 1
    print(strg)


def reverse_integer2(signed_integer):
    # python implementation
    strg_signed_integer = str(signed_integer)
    sign = 1
    if strg_signed_integer[0] == '-':
        sign = -1
        strg_signed_integer = strg_signed_integer[1:]
    strg_rev_signed_integer = strg_signed_integer[::-1]
    rev_signed_integer = sign * int(strg_rev_signed_integer)
    print(rev_signed_integer)


def reverse_integer1(signed_integer):
    # langauge independent (kind of) implementation
    integers = []
    sign = 1
    if signed_integer < 0:
        signed_integer = -1 * signed_integer
        sign = -1
        
    while signed_integer != 0:
        integers.append(signed_integer % 10)
        signed_integer = int(signed_integer / 10)
        #print(signed_integer)

    reversed_int = 0
    exponent = len(integers)
    for i, n in enumerate(integers):
        exponent -= 1
        reversed_int += n * (10 ** exponent)
    print(sign * reversed_int)


if __name__ == '__main__':
    x = bytearray(b'hello')
    reverse_str1(x)
    x = bytearray(b'hello world!')
    reverse_str1(x)
    print("=====")
    x = bytearray(b'hello')
    reverse_str2(x)
    x = bytearray(b'hello world!')
    reverse_str2(x)
    
    
    reverse_integer1(123)
    reverse_integer1(321)
    reverse_integer1(4800)
    reverse_integer1(-123)
    reverse_integer1(000)
    print("======")
    reverse_integer2(123)
    reverse_integer2(321)
    reverse_integer2(4800)
    reverse_integer2(-123)
    reverse_integer2(000)

