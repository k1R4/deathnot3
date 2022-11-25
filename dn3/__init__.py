from dn3.tools.config import *
from dn3.pwn import *
from dn3.misc import *
from dn3.tools import *
from dn3.l1ght import *
from dn3.crypto import *
from logging import getLogger, StreamHandler, Formatter, INFO, WARNING, ERROR
from sys import exit, stderr

def cli():
    CLIHandler()

class LoggerFormatter(Formatter):
    def format(self, record):
        prefix = ""
        if record.levelno == INFO:
            prefix = f"{BOLD}({BLUE}dn3{END}{BOLD}){END} "
        elif record.levelno == WARNING:
            prefix = f"{BOLD}({YELLOW}dn3{END}{BOLD}){END} "
        elif record.levelno == ERROR:
            prefix = f"{BOLD}({RED}dn3{END}{BOLD}){END} "
            print(f"{prefix}{REVERSE}{RED}{BOLD}\"{record.filename}\", {record.funcName}(): {END}{REVERSE}{RED}{record.msg}{END}",file=stderr)
            exit(1)
        else:
            prefix = f"{BOLD}({GREEN}dn3{END}{BOLD}){END} "
        return prefix +  super(LoggerFormatter, self).format(record)

handler = StreamHandler()
handler.setFormatter(LoggerFormatter("%(message)s"))
logger = getLogger(__name__)
logger.setLevel(INFO)
logger.addHandler(handler)