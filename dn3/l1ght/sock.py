from dn3.l1ght.pipe import *
from dn3.l1ght.context import *
from dn3.misc.colors import *
from dn3.tools.config import cfg
from dn3.misc.utils import msleep
from logging import getLogger
import socket

logger = getLogger(__name__)


class sock(BufferedPipe):

    def __init__(self, host, port=None):

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

        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self._host, self._port))
        except:
            logger.error("Unable to connect!")

        super().__init__()

        logger.info("Opened connection to %s%s:%s%s" % (BOLD,self._host,self._port,END))
        ctx.io = self


    def _read(self,n,timeout=int(cfg.timeout)):
        if not self._sock:
            logger.error("Socket closed!")

        self._sock.settimeout(timeout/1000)
        try:
            x = self._sock.recv(n)
            return x
        except socket.timeout:
            return b""
        except ConnectionAbortedError:
            self.kill()
            logger.error("Connection reset!")


    def _write(self,x):
        if not self._sock:
            logger.error("Socket closed!")
        try:
            return self._sock.send(x)
        except:
            logger.error("Socket closed unexpectedly!")


    def kill(self):
        if self._thread.is_alive():
            self._thread.join()
        self._sock.close()
        self._sock = None
        logger.info("Connection closed to %s:%s" % (self._host,self._port))


    def interactive(self):

        ctx.log = INFO
        print(self._buf.decode(),flush=True,end="")
        self._thread.start()

        while True:
            try:
                print("\r%s%sdn3>%s " % (YELLOW,BOLD,END), end="", flush=True)
                self.sendline(input())
                msleep(10)
                continue
            except:
                break

remote = sock