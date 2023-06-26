from dn3.misc.utils import *
from elftools.elf.elffile import ELFFile, SymbolTableSection, RelocationSection
from elftools.elf.elffile import SHN_INDICES
from logging import getLogger
import os

logger = getLogger(__name__)


class SymDict(object):


    def __init__(self,name,parent):
        self.__name__ = name
        self.__parent__ = parent


    def __getattribute__(self, key):
        if key.startswith("__") and key.endswith("__"):
            return object.__getattribute__(self,key)
        
        else:
            if key not in self.__dict__.keys():
                raise KeyError("Invalid %s symbol!" % (self.__name__))
            return object.__getattribute__(self,"__parent__").address - object.__getattribute__(self,"__parent__")._address + object.__getattribute__(self,key)
        

    def __getitem__(self,key):
        return object.__getattribute__(self,"__parent__").address - object.__getattribute__(self,"__parent__")._address + object.__getattribute__(self,key)


    def __str__(self):
        output = ""
        for key in self.__dict__.keys():

            if key.startswith("__") and key.endswith("__"):
                continue

            output += "%s(%s) => %s\n" % (self.__name__, key, hex(self.__dict__[key]))
        return output
    

    def __iter__(self):
        for attr in self.__dict__:
            if attr.startswith("__") and attr.endswith("__"):
                continue
            yield attr


class ELF():


    def __init__(self,path):

        if not path.startswith("/"):
            path = "%s/%s" % (os.getcwd(),path)

        self.path = path
        self.address = 0

        if not check_ELF(self.path):
            logger.error("Invalid ELF file!")

        self.arch = find_arch(self.path)

        if not self.arch:
            logger.error("Architecture not supported!")

        self._fd = open(self.path,"rb")
        self._elf = ELFFile(self._fd)
        self._sections = [ self._elf.get_section(i) for i in range(self._elf.num_sections()) ]
        self._sec_addrs = self._get_sec_addrs()
        self.address = 0
        self._address = self._sec_addrs[".text"]
        self._static = bool(".interp" not in self._sec_addrs and self._address != 0)

        self.symbols = SymDict("SYM",self)
        self.got = SymDict("GOT",self)
        self.plt = SymDict("PLT",self)

        self._get_symbols()
        self._get_got()
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

    
    def _get_got(self):

        if self._static:
            del self.got
            return

        for section in self._sections:

            if not isinstance(section,RelocationSection):
                continue

            if section.header.sh_link == SHN_INDICES.SHN_UNDEF:
                continue

            symbols = self._elf.get_section(section.header.sh_link)

            for reloc in section.iter_relocations():
                idx = reloc.entry.r_info_sym

                if not idx:
                    continue

                symbol = symbols.get_symbol(idx)

                if symbol and symbol.name:
                    setattr(self.got,symbol.name,reloc.entry.r_offset)

    def _get_plt(self):

        if self._static or not self.got:
            del self.plt
            return