from pwn import *
from logging import getLogger

logger = getLogger(__name__)


def str2bytes(x):
	if type(x) == str:
		return bytes([ord(i) for i in x])
	else:
		logger.error(f"{type(x)} provided, string expected!")


def bytes2str(x):
	if type(x) == bytes:
		return "".join([chr(i) for i in x])
	else:
		logger.error(f"{type(x)} provided, bytes expected!")


def pk(x):
	if type(x) == int:
		return bytes2str(pack(x,64)).rstrip("\x00")
	else:
		logger.error(f"{type(x)} provided, int expected!")


def pk64(x):
	if type(x) == int:
		return bytes2str(p64(x))
	else:
		logger.error(f"{type(x)} provided, int expected!")


def pk32(x):
	if type(x) == int:
		return bytes2str(p32(x))
	else:
		logger.error(f"{type(x)} provided, int expected!")


def upk(x):
	if type(x) == str:
		x = x.ljust(8,"\x00")
		return unpack(str2bytes(x),64)
	else:
		logger.error(f"{type(x)} provided, string expected!")


def flt(x):
	if type(x) == list:
		for i in range(len(x)):
			if type(x[i]) == str:
				x[i] = str2bytes(x[i])
		return bytes2str(flat(x))
	else:
		logger.error(f"{type(x)} provided, list expected")


def cyc(x):
	if type(x) == int:
		return bytes2str(cyclic(x))
	else:
		logger.error(f"{type(x)} provided, int expected!")