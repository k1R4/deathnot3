from dn3.l1ght.pipe import *
from dn3.l1ght.context import context
from logging import getLogger
from subprocess import Popen, PIPE, STDOUT
import os
import fcntl
import inspect

logger = getLogger(__name__)


class process(pipe):


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
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

        self._pid = self._process.pid

        super().__init__(self._process.stdout.read, self._process.stdin.write, self._process.stdin.flush)

        logger.info("Spawned process %s with PID: %d" % (self._cmd.split()[0],self._pid))


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
        self._process.kill()
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

    