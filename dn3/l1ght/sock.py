from dn3.l1ght.pipe import *
from dn3.l1ght.context import *
from dn3.misc.colors import *
from dn3.tools.config import cfg
from dn3.misc.utils import msleep
from logging import getLogger
import socket
import os
import fcntl

logger = getLogger(__name__)


class sock(pipe):

    def __init__(self, host, port=None, timeout=int(cfg.timeout)):

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

        super().__init__()

        logger.info("Opened connection to %s%s:%s%s" % (BOLD,self._host,self._port,END))
        ctx.io = self


    def _read(self,n):
        if not self._sock:
            logger.error("Socket closed!")
        blocked = 0
        while True:
            try:
                x = self._sock.recv(n)
                if not x:
                    raise Exception
                else:
                    return x
            except BlockingIOError:
                blocked += 1
                if blocked <= 100:
                    msleep(self._timeout//100)
                    continue
                else:
                    logger.error("Connection timed out!")
            except:
                logger.error("Socket closed unexpectedly!")


    def _write(self,x):
        if not self._sock:
            logger.error("Socket closed!")
        try:
            return self._sock.send(x)
        except:
            logger.error("Socket closed unexpectedly!")


    def recvall(self):
        x = b""
        t = None
        blocked = 0
        while True:
            try:
                t = self._sock.recv(1)
                if not t:
                    raise Exception
                else:
                    x += t
            except BlockingIOError:
                blocked += 1
                if blocked <= 100:
                    msleep(self._timeout//100)
                    continue
                else:
                    break
            except:
                break

        if ctx.log == DEBUG:
            IO_debug(x)

        if ctx.mode == str:
            x = bytes2str(x)
        
        return x


    def kill(self):
        self._sock.close()
        self._sock = None
        logger.error("Connection closed to %s:%s" % (self._host,self._port))


    def interactive(self):

        ctx.mode = bytes
        print(self.recvall().decode(), flush=True)
        while True:
            try:
                print("%s%sdn3>%s " % (YELLOW,BOLD,END), end="", flush=True)
                self.sendline(input())
                print(self.recvall().decode(), flush=True)
            except:
                return self.kill()


    def settimeout(self,n):
        self._timeout = n

remote = sock