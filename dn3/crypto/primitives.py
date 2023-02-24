from dn3.misc.encoding import *
from itertools import cycle

def xor(*args):
    result = [0]
    for arg in args:
        arg = list(x2bytes(arg))
        if hasattr(arg, '__iter__'):
            if len(arg) > len(result):
                result = [i^j for i,j in zip(arg, cycle(result))]
            else:
                result = [i^j for i,j in zip(result, cycle(arg))]
        else:
            result = [i^arg for i in result]
    return bytes(result)
        