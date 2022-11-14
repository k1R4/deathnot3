from abc import abstractmethod
from dn3.misc.encoding  import *
from dn3.l1ght.context import *
from logging import getLogger

logger = getLogger(__name__)


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
        
        if context.log == DEBUG:
            IO_debug(x)

        if context.mode == str:
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
        
        if context.log == DEBUG:
            IO_debug(t)

        if context.mode == str:
            t = bytes2str(t)
        
        return t

    
    def recvline(self):
        return self.recvuntil(b"\n")


    def send(self,x):
        x = x2bytes(x)

        if not x:
            logger.error("Invalid input")

        self._write(x)

        if context.log == DEBUG:
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
