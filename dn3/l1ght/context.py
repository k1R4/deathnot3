from typing import Any
from dn3.misc.colors import *
from dn3.tools.config import cfg
from logging import getLogger

logger = getLogger(__name__)

class Context():

    def __init__(self):
        self.log = 1
        self.arch = "amd64"
        self.io = None
        self.binary = None
        self.libc = None
        self.aslr = True
        self.mode = str
        self.terminal = cfg.terminal.split() if "terminal" in cfg.__dict__ else ""

    def __setattr__(self, key, value):
        if key == "binary" or key == "libc":
            if value == None:
                pass
            elif not hasattr(value,"arch"):
                logger.error("Invalid ELF!")
            elif value != None:
                setattr(self,"arch",getattr(value,"arch"))
        
        self.__dict__[key] = value


ctx = Context()