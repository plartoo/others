"""
Script to test if the bug mentioned in this article:
https://programming.guide/worlds-most-copied-so-snippet.html
happens in Python as well.
"""

import math


def human_readable_byte_count(bytes, si_or_not):
    unit = 1000 if si_or_not else 1024
    if bytes < unit:
        return ''.join([str(bytes), ' B'])

    exp = int(math.log(bytes) / math.log(unit))
    print(exp)

    pre_1 = 'kMGTPE'[exp-1] if si_or_not else 'KMGTPE'[exp-1]
    pre_2 = '' if si_or_not else 'i'
    pre = ''.join([pre_1, pre_2])
    print(pre)

    val = bytes / math.pow(unit, exp)
    print('%.1f %sB' % (val, pre))


if __name__ == '__main__':
    human_readable_byte_count(999949, True)
    human_readable_byte_count(999999, True)
    human_readable_byte_count(999949999999999999, True)

