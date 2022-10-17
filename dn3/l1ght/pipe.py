from abc import abstractmethod
from dn3.misc.encoding  import *
from dn3.l1ght.context import *
from dn3.misc.utils import msleep
from logging import getLogger

logger = getLogger(__name__)


class pipe():


    def __init__(self, read, write, flush=None):

        self._read = read
        self._write = write
        self._flush = flush


    @abstractmethod
    def kill():
        pass

    
    @abstractmethod
    def _poll():
        pass


    @abstractmethod
    def interactive():
        pass


    def _recv(self,n):
        waits = 0
        x = b""
        while True:
            try:
                x = self._read(n)
                if not x and self._poll():
                    msleep(1)
                else:
                    break
            except BlockingIOError:
                if waits > 5:
                    break
                else:
                    waits += 1
                    msleep(10)
                    continue
        return x


    def recvall(self):
        x = b""
        consecutive_null = 0
        while True:
            try:
                c = self._recv(1)
                if not c:
                    consecutive_null += 1
                    msleep(1)
                    if consecutive_null > 3:
                        break
                else:
                    x += c
                    consecutive_null = 0
            except:
                break

        if not x:
            self._poll()

        if context.log == DEBUG:
            debug(x)

        if context.mode == str:
            x = bytes2str(x)
        
        return x


    def recv(self, n):
        
        x = self._recv(n)
        
        if context.log == DEBUG:
            debug(x)

        if context.mode == str:
            x = bytes2str(x)

        return x

    
    def recvuntil(self,x):

        x = x2bytes(x)
        t = b""

        if not x:
            logger.error("Invalid delimiter length!")

        while True:
            k = self._recv(1)
            if not k:
                self._poll()
                msleep(1)
                continue

            t += k
            if t.find(x) != -1:
                break
        
        if context.log == DEBUG:
            debug(t)

        if context.mode == str:
            t = bytes2str(t)
        
        return t

    
    def recvline(self):
        return self.recvuntil(b"\n")


    def send(self,x):
        x = x2bytes(x)

        if not x:
            logger.error("Invalid input")

        if self._poll():
            self._write(x)
            if self._flush:
                self._flush()

        if context.log == DEBUG:
            debug(x, "Sent")


    def sendline(self, x):
        x = x2bytes(x) + b"\n"
        self.send(x)


    def sendafter(self, d, x):
        self.recvuntil(d)
        self.send(x)


    def sendlineafter(self, d, x):
        self.recvuntil(d)
        self.sendline(x)
