from dn3.l1ght.pipe import *
from dn3.l1ght.context import context
from logging import getLogger
import socket
from sys import stdout
import os
import fcntl

logger = getLogger(__name__)


class sock(pipe):

    def __init__(self, host, port=None, timeout=10):

        try:
            if host.startswith("nc "):
                _, host, port = host.split()
            
            if ":" in host:
                host, port = host.split(":")

            port = int(port)
        except:
            logger.error("Invalid host/port!")

        self._host = host
        self._port = port
        self._timeout = timeout

        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._host, self._port))
        except:
            logger.error("Unabled to connect!")

        fd = self._sock.fileno()
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        super().__init__(self._sock.recv, self._sock.send)


    def _poll(self):
        return True


    # def recvall(self):
    #     return self._pipe.recvall()


    # def recv(self,n):
    #     return self._pipe.recv(n)


    # def recvuntil(self,x):
    #     return self._pipe.recvuntil(x)


    # def recvline(self):
    #     return self._pipe.recvline()


    # def send(self,x):
    #     return self._pipe.send(x)


    # def sendline(self, x):
    #     return self._pipe.sendline(x)


    # def sendafter(self, d, x):
    #     return self._pipe.sendafter(d,x)


    # def sendlineafter(self, d, x):
    #     return self._pipe.sendlineafter(d,x)


    def kill(self):
        self._sock.close()
        logger.error("Connection closed to %s:%s" % (self._host,self._port))


    def interactive(self):

        context.mode = bytes
        print(self.recvall().decode(), flush=True)
        while True:
            try:
                print("%s%sdn3>%s " % (YELLOW,BOLD,END), end="", flush=True)
                self.sendline(input())
                print(self.recvall().decode(), flush=True)
            except:
                return self.kill()

        
