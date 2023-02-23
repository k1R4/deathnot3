from struct import *
from logging import getLogger

logger = getLogger(__name__)

def ascii(x):
	return "".join([i for i in x if ord(i) < 0x7f])

def alnumsym(x):
	return "".join([i for i in x if ord(i) > 0x20 and ord(i) < 0x7f])


def dotalnumsym(x):
	t = ""
	for c in x:
		if ord(c) > 0x21 and ord(c) < 0x7f:
			t += c
		else:
			t += "."
	return t


def x2sb(x,mode=str):
	if mode == str:
		return x2str(x)
	else:
		return x2bytes(x)


def x2str(x):
	if isinstance(x,bytes):
		return bytes2str(x)
	elif isinstance(x,int):
		return str(x)
	elif isinstance(x,str):
		return x
	else:
		logger.error("%s provided, bytes/int/string expected!" % type(x))


def x2bytes(x):
	if isinstance(x,bytes):
		return x
	elif isinstance(x,int):
		return str2bytes(str(x))
	elif isinstance(x,str):
		return str2bytes(x)
	else:
		logger.error("%s provided, bytes/int/string expected!" % type(x))


def str2bytes(x):
	if isinstance(x,str):
		return bytes([ord(i) for i in x])
	else:
		logger.error("%s provided, string expected!" % type(x))


def bytes2str(x):
	if isinstance(x,bytes):
		return "".join([chr(i) for i in x])
	else:
		logger.error("%s provided, bytes expected!" % type(x))


def pk(x):
	if isinstance(x,int):
		return bytes2str(pack("<Q", x)).rstrip("\x00")
	else:
		logger.error("%s provided, int expected!" % type(x))


def p64(x):
	if isinstance(x,int):
		return bytes2str(pack("<Q", x))
	else:
		logger.error("%s provided, int expected!" % type(x))


def p32(x):
	if isinstance(x,int):
		return bytes2str(pack("<L",x))
	else:
		logger.error("%s provided, int expected!" % type(x))


def p16(x):
	if isinstance(x,int):
		return bytes2str(pack("<H",x))
	else:
		logger.error("%s provided, int expected!" % type(x))


def upk(x):
	if isinstance(x,str):
		return unpack("<Q",str2bytes((x[:8]).ljust(8,"\x00")))[0]
	elif isinstance(x,bytes):
		return unpack("<Q",(x[:8]).ljust(8,b"\x00"))[0]
	else:
		logger.error("%s provided, string expected!" % type(x))


def flat(x, arch="amd64"):
	out = ""

	if isinstance(x,list):
		for i in x:
			if isinstance(i,str):
				out += i
			elif isinstance(i,bytes):
				out += bytes2str(i)
			elif isinstance(i,int):
				if arch == "amd64":
					out += p64(i)
				else:
					out += p32(i)
		return out
	else:
		logger.error("%s provided, list expected" % type(x))