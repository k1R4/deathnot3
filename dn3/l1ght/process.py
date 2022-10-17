from dn3.misc.encoding  import *
from dn3.l1ght.context import *
from dn3.misc.utils import msleep
from logging import getLogger
from subprocess import Popen, PIPE, STDOUT
import os
import fcntl

logger = getLogger(__name__)


class process():


    def __init__(self,cmd):

        self._cmd = cmd
        if self._cmd.startswith("./"):
            self._cmd = "%s/%s" % (os.getcwd(),self._cmd[2:])

        try:
            self._process = Popen(self._cmd.split(), 
                                    stdin = PIPE,
                                    stdout = PIPE,
                                    stderr = STDOUT)
        except:
            logger.error("File not found!")

        fd = self._process.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        self._pid = self._process.pid
        self._buf = None
        logger.info("Spawned process %s with PID: %d" % (self._cmd.split()[0],self._pid))


    def _poll(self):

        if self._process.poll() is None and self._process.stdout.readable():
            return True
        else:
            logger.error("Process %s stopped with code: %d" % (self._cmd.split()[0],self._process.returncode))


    def recvall(self):
        x = b""
        consecutive_null = 0
        while True:
            try:
                c = self._process.stdout.read(1)
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


    def recv(self,n):
        while True:
            x = self._process.stdout.read(n)
            if not x:
                self._poll()
                msleep(1)
            break
        
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
            k = self._process.stdout.read(1)
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
            self._process.stdin.write(x)
            self._process.stdin.flush()

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

    
    def kill(self):
        self._process.kill()
        logger.info("Process %s with PID: %d was killed!" % (self._cmd.split()[0], self._pid))


    def interactive(self):

        print(self.recvall(), flush=True)
        while True:
            if self._poll():
                try:
                    print("$ ", end="", flush=True)
                    self._process.stdin.write(str2bytes(input()+"\n"))
                    self._process.stdin.flush()
                    if self._poll():
                        print(self.recvall(), flush=True)
                except:
                    self.kill()

    