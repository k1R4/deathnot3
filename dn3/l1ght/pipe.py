from abc import abstractmethod
from dn3.tools.config import cfg
from dn3.l1ght.context import ctx
from dn3.misc.encoding import *
from dn3.misc.colors import *
from dn3.misc.utils import msleep
from threading import Thread, Lock
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


class BufferedPipe():


    def __init__(self):
        self._buf = b""
        self._max_buf = 4096
        self._thread = Thread(target=self._interactive_output)
        self._thread.daemon = True

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


    def _interactive_output(self):

        if hasattr(self, "_sock"):
            timeout = int(cfg.timeout)
        else:
            timeout = 0.1

        while True:
                x = self._read(4096,timeout)
                if x:
                    try:
                        x = x.decode()
                    except:
                        x = bytes2str(x)
                    print("\r"+x,end="",flush=True)
                    print("%s%sdn3>%s " % (YELLOW,BOLD,END), end="", flush=True)


    def recv(self, n, timeout=None):
        
        if n > 4096:
            logger.error("Can only recv 4096 bytes at a time")

        x = b""
        
        if n > len(self._buf):
            x += self._buf
            if not timeout:
                self._buf = self._read(self._max_buf)
            else:
                self._buf = self._read(self._max_buf,timeout)
            n -= len(x)

        x += self._buf[:n]
        self._buf = self._buf[n:]

        if len(x) != n:
            logger.error("EOF!")

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

        n = self._buf.find(x)
        if n == -1:
            t = self._buf
            self._buf = b""
            while True:
                k = self._read(1)
                if not k:
                    logger.error("EOF!")
                t += k
                if t.find(x) != -1:
                    break

        else:
            t = self._buf[:n+len(x)]
            self._buf = self._buf[n+len(x):]
        
        if ctx.log == DEBUG:
            IO_debug(t)

        if ctx.mode == str:
            t = bytes2str(t)
        
        return t

    
    def recvline(self):
        return self.recvuntil(b"\n")

    def recvall(self):

        x = self._buf
        self._buf = b""

        if ctx.log == DEBUG:
            IO_debug(x)

        if ctx.mode == str:
            x = bytes2str(x)

        return x

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
