from struct import *
from logging import getLogger

logger = getLogger(__name__)


def ascii(x):
	return "".join([i for i in x if ord(i) > 0x20 and ord(i) < 0x7f])


def dotascii(x):
	t = ""
	for c in x:
		if ord(c) > 0x21 and ord(c) < 0x7f:
			t += c
		else:
			t += "."
	return t
		

def x2str(x):
	if type(x) == bytes:
		return bytes2str(x)
	elif type(x) == int:
		return str(x)
	elif type(x) == str:
		return x
	else:
		logger.error("%s provided, bytes/int/string expected!" % type(x))


def x2bytes(x):
	if type(x) == bytes:
		return x
	elif type(x) == int:
		return str2bytes(str(x))
	elif type(x) == str:
		return str2bytes(x)
	else:
		logger.error("%s provided, bytes/int/string expected!" % type(x))


def str2bytes(x):
	if type(x) == str:
		return bytes([ord(i) for i in x])
	else:
		logger.error("%s provided, string expected!" % type(x))


def bytes2str(x):
	if type(x) == bytes:
		return "".join([chr(i) for i in x])
	else:
		logger.error("%s provided, bytes expected!" % type(x))


def pk(x):
	if type(x) == int:
		return bytes2str(pack("<Q", x)).rstrip("\x00")
	else:
		logger.error("%s provided, int expected!" % type(x))


def p64(x):
	if type(x) == int:
		return bytes2str(pack("<Q", x))
	else:
		logger.error("%s provided, int expected!" % type(x))


def p32(x):
	if type(x) == int:
		return bytes2str(pack("<L",x))
	else:
		logger.error("%s provided, int expected!" % type(x))


def p16(x):
	if type(x) == int:
		return bytes2str(pack("<H",x))
	else:
		logger.error("%s provided, int expected!" % type(x))

def upk(x):
	if type(x) == str:
		return unpack("<Q",str2bytes((x[:8]).ljust("\x00",8)))
	elif type(x) == bytes:
		return unpack("<Q",(x[:8]).ljust(b""))
	else:
		logger.error("%s provided, string expected!" % type(x))


def flat(x, arch="amd64"):
	out = ""

	if type(x) == list:
		for i in list:
			if type(i) == str:
				out += i
			elif type(i) == bytes:
				out += bytes2str(i)
			elif type(i) == int:
				if arch == "amd64":
					out += p64(i)
				else:
					out += p32(i)
		return out
	else:
		logger.error("%s provided, list expected" % type(x))