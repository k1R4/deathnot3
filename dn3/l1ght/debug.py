from dn3.l1ght.pipe import *
from dn3.l1ght.proc import *
from dn3.misc.colors import *
from dn3.tools.config import cfg
from logging import getLogger
import string
import random
import subprocess
import sys

logger = getLogger(__name__)

class debug(proc):

    def __init__(self, path, gdbscript="", port=cfg.gdbport, env=None):

        if not ctx.terminal:
            logger.error("ctx.terminal hasn't been set")
        elif type(ctx.terminal) != list:
            logger.error("Expected ctx.terminal as list")

        self._path = path
        self._port = port
        self._cmd = "/bin/gdbserver --once "
        if ctx.aslr:
            self._cmd += "--no-disable-randomization "
        self._cmd += "localhost:%s %s" % (self._port, self._path)

        try:

            super().__init__(self._cmd, env=env)
            self.recvline()
            self.recvline()
            logger.info("GDBServer listening for connection on port %s%s%s" % (BOLD,self._port,END))

        except:
            logger.error("Failed to start gdbserver!")

        try:
            gdbscript = ("target remote:%s\n" % self._port) + gdbscript.lstrip("\n").rstrip("\n") + "\n"
            self._script = "".join(random.choice(string.ascii_letters) for _ in range(10))
            self._script = "/tmp/%s" % self._script
            f = open(self._script, "w+")
            f.write(gdbscript)
            f.close()

            self._term = subprocess.Popen(ctx.terminal + ["gdb","-x",self._script], stdout=sys.stdout, stdin=sys.stdin, stderr=sys.stderr)

            self.recvline()
            logger.info("Recieved connection from GDB client!")
            ctx.io = self

        except:
            logger.error("Failed to spawn terminal!")


    def kill(self):
        super().kill()
        self._term.terminate()

gdb = debug
