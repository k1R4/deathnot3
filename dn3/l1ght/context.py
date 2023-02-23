from dn3.misc.colors import *
from dn3.tools.config import config


class Context():

    def __init__(self):
        self.log = 1
        self.arch = "amd64"
        self.io = None
        self.binary = None
        self.libc = None
        self.aslr = True
        self.mode = str
        self.terminal = config.terminal.split() if "terminal" in config.__dict__ else ""


ctx = Context()