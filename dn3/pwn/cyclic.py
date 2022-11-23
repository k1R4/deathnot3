from dn3.misc.encoding import *
from logging import getLogger
from binascii import unhexlify

logger = getLogger(__name__)

pattern_dict = ["d", "e", "a", "7", "h", "n", "o", "t", "3", "l", "1", "g", "h", "t"]


def cyclic(n=None, dict=pattern_dict):

    if dict != pattern_dict:
        if not isinstance(dict, (list,tuple)):
            logger.error("Invalid pattern list!")
        for i in dict:
            if dict.count(i) > 1:
                logger.error("Pattern list shouldn't contain duplicates")
    
    if len(pattern_dict) > len(dict):
        logger.error("Provide larger dictionary!")

    if not n:
        n = 8192
    if not isinstance(n, int):
        logger.error("Integer expected!")
    if n > 8192:
        logger.error("Size must not be greater than 8192")
    if n%4 != 0:
        logger.error("Size must be multiple of 4")

    out = ""
    length = 0
    for i in dict:
        for j in dict:
            for k in dict:
                for l in dict:
                    out += l + k + j + i
                    length += 4
                    if length == n:
                        return out


def cyclic_find(x, dict=pattern_dict):
    if isinstance(x,int):
        x = unhexlify(hex(x)[2:])
    x = x2str(x)
    if not isinstance(x, str) or len(x) != 4:
        logger.error("String of length 4 expected!")
    x = x[::-1]
    offset = cyclic(8192,dict).find(x) 
    if offset == -1:
        logger.error("Invalid pattern!")
    else:
        return offset


def CyclicHandler(arg):
    try:
        arg = int(arg)
    except:
        if arg.startswith("0x"):
            arg = unhexlify(arg[2:])
    if isinstance(arg,(bytes,str)):
        logger.info("Offset: %s" % cyclic_find(arg))
    elif isinstance(arg,int):
        print(cyclic(arg))
