from dn3.misc.colors import *
from logging import getLogger
from subprocess import DEVNULL, check_call
from shutil import copy2, copystat
import zstandard
from time import sleep
from os import getcwd

logger = getLogger(__name__)


def dn3_exists(deathnote):

	if deathnote == None or deathnote.io == None:
		deathnote = None
		logger.error("deathnot3 is not initialized or process died")
		return False
	else:
		return True


def dn3_libc_exists(deathnote):

	if deathnote == None or deathnote.libc == None:
		logger.error("Libc ELF not provided during initialization")
		return False
	else:
		return True


def check_ELF(file):
	header = open(file,"rb").read(0x4)
	if header != b"\x7f\x45\x4c\x46":
		return False
	else:
		return True


def find_arch(file):
	arch_byte = open(file,"rb").read(0x13)[0x12]
	if arch_byte == 0x3e:
		return "amd64"
	elif arch_byte == 0x3:
		return "i386"
	else:
		return False


def sh(cmd):
	try:
		check_call(cmd.split(), stdout=DEVNULL, stderr=DEVNULL, cwd=getcwd())
		return True
	except:
		return False


def copy(src,dst):
	try:
		copy2(src,dst)
		copystat(src,dst)
		return True
	except IOError as e:
		logger.error("Unable to copy file. %s" % e)


def extract_zst(file,dir,out):
	zstd = zstandard.ZstdDecompressor()
	tarball = open(f"{dir}{out}","wb+")
	zstd.copy_stream(file, tarball)
	tarball.seek(0)
	return tarball


def msleep(x):
	return sleep((1/1000)*x)


def dn3_prompt(x):
	return input("%s(%sdn3%s%s)%s %s" % (BOLD,PURPLE,END,BOLD,END,x)).rstrip("\n")

def pause():
	return dn3_prompt("Press [Enter]")