from dn3.misc.colors import *
from dn3.misc.encoding import *
from dn3.config import config
from binascii import hexlify

DEBUG = 1
L1GHT = 0


def IO_debug(x, mode="Received"):
    if not x:
        return

    if mode == "Received":
        color = RED
    else:
        color = CYAN


    print("%s%s[L1GHT]%s %s %d bytes:" % (color, BOLD, END, mode, len(x)), end="")

    i,j = 0,-1
    while i < len(x):

        j += 1
        if not j%27:
            if i >= 24:
                print("  %s|%s  %s" % (BLUE, END, dotalnumsym(bytes2str(x[i-24:i]))), end="")
            print("\n        ", end="")
            continue

        if not j%9:
            print("  ", end="")
            continue

        print(bytes2str(hexlify(bytes([x[i]]))), end="")
        i += 1

    k = i%24
    if k:
        print("  "*(27 - j%27 - 1), end="")
    else:
        k = 24
    print("  %s|%s  %s" % (BLUE, END, dotalnumsym(bytes2str(x[len(x)-k:len(x)]))))

    


class Context():


    def __init__(self):
        self.log = DEBUG
        self.arch = "amd64"
        self.io = None
        self.binary = None
        self.libc = None
        self.aslr = True
        self.mode = str
        self.terminal = config.terminal.split() if "terminal" in config.__dict__ else ""


context = Context()