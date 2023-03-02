from abc import abstractmethod
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

IOs = []


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
        self._is_interactive = False
        self._run_thread = True
        self._lock = Lock()
        self._thread = Thread(target=self._reader)
        self._thread.daemon = True
        self._thread.start()

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


    def _reader(self):

        while self._run_thread:
            if len(self._buf) < self._max_buf:
                x = b""
                self._lock.acquire()
                x = self._read(self._max_buf-len(self._buf),timeout=5)
                if x:
                    if self._is_interactive:
                        print(x.decode(),end="",flush=True)
                    else:
                        self._buf += x
                    self._lock.release()
                    msleep(1)
                    continue
                else:
                    self._lock.release()
                    msleep(1)
                    continue

    def recv(self, n, timeout=1000):
        
        x = b""

        self._lock.acquire()
        if n > len(self._buf):
            x += self._buf
            self._buf = b""
            x += self._read(n-len(x),timeout)

        else:
            x += self._buf[:n]
            self._buf = self._buf[n:]

        if len(x) != n:
            logger.error("EOF!")

        if ctx.log == DEBUG:
            IO_debug(x)

        if ctx.mode == str:
            x = bytes2str(x)

        self._lock.release()
        return x

    
    def recvuntil(self,x):

        x = x2bytes(x)
        t = b""

        if not x:
            logger.error("Invalid delimiter length!")

        mode,log = ctx.mode,ctx.log
        ctx.mode,ctx.log = bytes,INFO
        while True:
            k = self.recv(1)
            t += k
            if t.find(x) != -1:
                break
        ctx.mode,ctx.log = mode,log
        
        if ctx.log == DEBUG:
            IO_debug(t)

        if ctx.mode == str:
            t = bytes2str(t)
        
        return t

    
    def recvline(self):
        return self.recvuntil(b"\n")

    def recvall(self):
        self._lock.acquire()
        x = self._buf
        self._buf = b""

        if ctx.log == DEBUG:
            IO_debug(x)

        if ctx.mode == str:
            x = bytes2str(x)

        self._lock.release()
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
