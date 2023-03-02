from dn3.misc.utils import *
from elftools.elf.elffile import ELFFile, SymbolTableSection
from logging import getLogger
import os

logger = getLogger(__name__)


class SymDict(object):

    def __init__(self,parent):
        self._parent = parent

    def __getattribute__(self, key):
        if key == "_parent":
            return object.__getattribute__(self,key)
        else:
            return object.__getattribute__(self,"_parent").address - object.__getattribute__(self,"_parent")._address + object.__getattribute__(self,key)
        
    def __getitem__(self,key):
        return object.__getattribute__(self,"_parent").address - object.__getattribute__(self,"_parent")._address + object.__getattribute__(self,key)



class ELF():


    def __init__(self,path):

        if not path.startswith("/"):
            path = "%s/%s" % (os.getcwd(),path)

        self.path = path
        self.address = 0

        if not check_ELF(self.path):
            logger.error("Invalid ELF file!")

        self._arch = find_arch(self.path)

        if not self._arch:
            logger.error("Architecture not supported!")

        self._fd = open(self.path,"rb")
        self._elf = ELFFile(self._fd)
        self._sections = [ self._elf.get_section(i) for i in range(self._elf.num_sections()) ]
        self._sec_addrs = self._get_sec_addrs()

        self.address = 0
        self._address = self._sec_addrs[".text"]
        self.symbols = SymDict(self)

        self._get_symbols()
        logger.info("Loaded ELF : %s%s%s" % (BOLD,self.path.split("/")[-1],END))


    def _get_sec_addrs(self):

        addrs = {}
        for section in self._sections:
            addr = section.header.sh_addr - section.header.sh_offset
            if addr < 0:
                addr = 0
            addrs[section.name] = addr

        return addrs


    def _get_symbols(self):

        for section in self._sections:

            if not isinstance(section,SymbolTableSection):
                continue

            for symbol in section.iter_symbols():
                if not symbol.entry.st_value:
                    continue
                else:
                    setattr(self.symbols,symbol.name,symbol.entry.st_value)