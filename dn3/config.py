from dn3.misc.utils import *
from logging import getLogger
import os

logger = getLogger(__name__)


class Config():
    

    def __init__(self):
        self._path = "%s/.dn3.conf" % os.getenv("HOME")
        self.keys = ["template", "gdbport", "timeout"]
        self.vals = ["https://raw.githubusercontent.com/k1R4/deathnot3/dev/template.py", "1337", "800"]
        self.read()


    def create(self):
        conf = ""
        for i in range(len(self.keys)):
            conf += "%s = %s\n" % (self.keys[i], self.vals[i])
        f = open(self._path, "w+")
        f.write(conf)
        f.close()


    def read(self):
        if not os.path.exists(self._path):
            self.create()

        f = open(self._path, "r")
        for i in f.readlines():
            key, _, val = i.rstrip("\n").split()
            setattr(self, key, val)

        for i in range(len(self.keys)):
            try:
                getattr(self, self.keys[i])
            except:
                setattr(self, self.keys[i], self.vals[i])
        
        f.close()
    

    def write(self, argv):
        conf = ""

        if len(argv) == 3:
            f = open(self._path, "r+")
            conf = f.read()
            conf = conf.split("\n")[:-1]
            f.close()

            setattr(self, argv[2], dn3_prompt("%s: " % argv[2]))
            if getattr(self, argv[2]) == "" and argv[2] not in self.keys:
                delattr(self,argv[2])
                for i in range(len(conf)):
                    if argv[2] == conf[i].split()[0]:
                        conf.remove(conf[i])
                        conf = "\n".join(conf)+"\n"
                        f = open(self._path, "w+")
                        f.write(conf)
                        f.close()
                        return

            for i in range(len(conf)):
                if argv[2] == conf[i].split()[0]:
                    conf[i] = "%s = %s" % (argv[2], getattr(self, argv[2]))
                    f = open(self._path, "w+")
                    f.write("\n".join(conf)+"\n")
                    f.close()
                    return

            conf = "%s = %s\n" % (argv[2], getattr(self, argv[2]))
            f = open(self._path, "a")
            f.write(conf)
            f.close()
            return

        else:
            f = open(self._path, "r")
            conf = f.read().split("\n")[:-1]
            f.close()

            for i in conf:
                key, _, val = i.split()
                if key not in self.keys:
                    self.keys.append(key)
                    self.vals.append(val)
            conf = ""

            for i in range(len(self.keys)):
                fancy_i = self.keys[i].replace("_", " ").capitalize()
                setattr(self, self.keys[i], dn3_prompt("%s (%s): " % (fancy_i,self.vals[i])))
                
                if getattr(self, self.keys[i]) in ["Y", "y", ""]:
                    setattr(self, self.keys[i], self.vals[i])

                conf += "%s = %s\n" % (self.keys[i],getattr(self, self.keys[i]))

            f = open(self._path, "w+")
            f.write(conf)
            f.close()


config = Config()