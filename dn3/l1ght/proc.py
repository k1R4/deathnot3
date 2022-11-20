from dn3.l1ght.pipe import *
from dn3.l1ght.context import context
from dn3.misc.colors import *
from dn3.misc.utils import msleep
from logging import getLogger
from subprocess import Popen, PIPE, STDOUT
import os
import fcntl
import tty
import pty

logger = getLogger(__name__)


class proc(pipe):


    def __init__(self,cmd,env=None):

        self._cmd = cmd
        if not self._cmd.startswith("/"):
            if self._cmd.startswith("./"):
                self._cmd = self._cmd[2:]
            self._cmd = "%s/%s" % (os.getcwd(),self._cmd)

        try:

            master, self._slave = pty.openpty()
            tty.setraw(master)
            tty.setraw(self._slave)

            if not env:
                env = os.environ.copy()

            self._process = Popen(self._cmd.split(), 
                                    stdin = PIPE,
                                    stdout = self._slave,
                                    stderr = STDOUT,
                                    cwd = os.getcwd(),
                                    env = env)
        except:
            logger.error("File not found or insufficient permissions!")

        

        if master:
            self._process.stdout = os.fdopen(os.dup(master), 'r+b', 0)
            os.close(master)
        
        fd = self._process.stdout.fileno()
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        self._pid = self._process.pid

        super().__init__()

        logger.info("Spawned process %s with PID: %s%d%s" % (self._cmd.split()[0],BOLD,self._pid,END))
        context.io = self


    def _read(self,n):
        if not self._process:
            logger.error("Process Ended!")
        x = b""
        while True:
            x = self._process.stdout.read(n)
            if not x and self._poll():
                msleep(1)
            else:
                break
        return x

    
    def _write(self,x):
        self._process.stdin.write(x)
        self._process.stdin.flush()  


    def recvall(self):
        x = b""
        t = None
        blocked = 0
        while True:
            try:
                t = self._process.stdout.read(1)
                if not t and blocked < 5:
                    blocked += 1
                    msleep(5)
                elif blocked >= 5:
                    break
                else:
                    x += t
                    blocked = 0
                    t = None
            except:
                break

        if not x:
            self._poll()

        if context.log == DEBUG:
            IO_debug(x)

        if context.mode == str:
            x = bytes2str(x)
        
        return x


    def _poll(self):

        if self._process and self._process.poll() is None and self._process.stdout.readable():
            return True
        else:
            if self._process:
                returncode = self._process.returncode
                self._process = None
                logger.error("Process %s stopped with code: %d" % (self._cmd.split()[0],returncode))
            return False


    def kill(self):
        if not self._process:
            return
        self._process.terminate()
        self._process = None
        logger.info("Process %s with PID: %d was killed!" % (self._cmd.split()[0], self._pid))


    def interactive(self):

        context.mode = bytes
        print(self.recvall().decode(), flush=True)
        while True:
            if self._poll():
                try:
                    print("%s%sdn3>%s " % (YELLOW,BOLD,END), end="", flush=True)
                    self.sendline(input())
                    if self._poll():
                        print(self.recvall().decode(), flush=True)
                except:
                    self.kill()
                    return
            else:
                break

    
process = proc