from abc import abstractmethod
from dn3.l1ght.context import ctx
from dn3.misc.encoding import *
from dn3.misc.colors import *
from logging import getLogger
from binascii import hexlify

logger = getLogger(__name__)


DEBUG = 1
INFO = 0


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


class pipe():


    def __init__(self):
        self.buf = b""

    @abstractmethod
    def kill():
        pass

    @abstractmethod
    def interactive():
        pass

    @abstractmethod
    def _read():
        pass

    @abstractmethod
    def _write():
        pass

    @abstractmethod
    def recvall():
        pass


    def recv(self, n):
        
        x = self._read(n)
        
        if ctx.log == DEBUG:
            IO_debug(x)

        if ctx.mode == str:
            x = bytes2str(x)

        return x

    
    def recvuntil(self,x):

        x = x2bytes(x)
        t = b""

        if not x:
            logger.error("Invalid delimiter length!")

        while True:
            k = self._read(1)
            t += k
            if t.find(x) != -1:
                break
        
        if ctx.log == DEBUG:
            IO_debug(t)

        if ctx.mode == str:
            t = bytes2str(t)
        
        return t

    
    def recvline(self):
        return self.recvuntil(b"\n")


    def send(self,x):
        x = x2bytes(x)

        if not x:
            logger.error("Invalid input")

        self._write(x)

        if ctx.log == DEBUG:
            IO_debug(x, "Sent")


    def sendline(self, x):
        x = x2bytes(x) + b"\n"
        self.send(x)


    def sendafter(self, d, x):
        self.recvuntil(d)
        self.send(x)


    def sendlineafter(self, d, x):
        self.recvuntil(d)
        self.sendline(x)
