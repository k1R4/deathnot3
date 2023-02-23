from dn3.misc.utils import *
from dn3.misc.encoding import *
from logging import getLogger
from threading import Thread
import os

logger = getLogger(__name__)


class Config():


    def __setattr__(self,key,value):
        if value == "" and key not in self._defaults.keys():
            try:
                getattr(self,key)
                return delattr(self,key)
            except:
                return
        self.__dict__[key] = value
        if not self._lock:
            self.update()
    
    def __delattr__(self,key):
        del self.__dict__[key]
        if not self._lock:
            self.update()


    def __init__(self):
        self._lock = 1
        self._path = "%s/.dn3.conf" % os.getenv("HOME")
        self._defaults = {"template": "https://raw.githubusercontent.com/k1R4/deathnot3/dev/template.py",
                          "gdbport" : "1337", 
                          "timeout" : "800",
                          "terminal": "tmux new-window"}
        self._thread = Thread(target=self.read(),args=(self,))


    def update(self):
        try:
            conf = ""
            for i in self.__dict__:
                if i.startswith("_"):
                    continue
                conf += "%s = %s\n" % (i, self.__dict__[i])
            f = open(self._path, "w+")
            f.write(conf)
            f.close()
        except Exception as e:
            print(e)
            return


    def setdefaults(self):
        for key,val in self._defaults.items():
            try:
                getattr(self,key)
            except:
                setattr(self,key,val)


    def read(self):
        self._lock = 1

        self.setdefaults()

        if not os.path.exists(self._path):
            self._lock = 0
            return

        f = open(self._path, "r")
        for i in f.readlines():
            i  = i.rstrip("\n").split()
            key, val = i[0], " ".join(i[2:])
            setattr(self, key, val)
        f.close()
        self._lock = 0
    

    def write(self, argv):
        self._lock = 1

        if len(argv) == 3:
            setattr(self, argv[2], dn3_prompt("%s: " % argv[2]))

        else:
            for i in self.__dict__:
                if i.startswith("_"):
                    continue
                fancy_i = i.replace("_", " ").capitalize()
                setattr(self, i, dn3_prompt("%s (%s): " % (fancy_i,self.__dict__[i])))
                
                if getattr(self, i) in ["Y", "y", ""]:
                    setattr(self, i, self.vals[i])

        self._lock = 0


cfg = Config()