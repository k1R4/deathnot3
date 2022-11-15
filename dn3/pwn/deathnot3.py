from pwn import ELF
from dn3.misc.encoding import *
from dn3.misc.utils import *
from dn3 import l1ght
from dn3.l1ght.context import context
from logging import getLogger
import os

logger = getLogger(__name__)

deathnote = None

class DeathNot3():

	def __init__(self,io=context.io,libc=context.libc):

		global deathnote

		if context.binary == None:
			logger.warn("(context.binary) has not been set")

		if not isinstance(io, (l1ght.proc, l1ght.sock, l1ght.debug)):
			logger.error("Pipe provided isn't a l1ght entity")

		if isinstance(libc, ELF):
			logger.warn("Provided libc isn't a pwnlib ELF")

		self.binary = context.binary
		self.io = io
		self.libc = libc
		deathnote = self

		logger.info("deathnot3 has been initialized!")


def rec(n):
	if dn3_exists(deathnote):
		return deathnote.io.recv(n)

def reu(s):
	if dn3_exists(deathnote):
		return deathnote.io.recvuntil(s)

def rl():
	if dn3_exists(deathnote):
		return deathnote.io.recvline()

def s(s):
	if dn3_exists(deathnote):
		return deathnote.io.send(s)

def sl(s):
	if dn3_exists(deathnote):
		return deathnote.io.sendline(s)

def sa(d,s):
	if dn3_exists(deathnote):
		return deathnote.io.sendafter(d,s)

def sla(d,s):
	if dn3_exists(deathnote):
		return deathnote.io.sendlineafter(d,s)

def interactive():
	global deathnote
	if dn3_exists(deathnote):
		deathnote.io.interactive()
		deathnote = None
		return

def intleak(length=14):
	return int(deathnote.io.recv(length),16)

def byteleak(length=6):
	return unpack(str2bytes(deathnote.io.recv(length)),length*8)


def libcleak(sym=0,length=6):

	if dn3_libc_exists(deathnote):

		leak = byteleak(length)
		if isinstance(sym, str):
			leak = leak - deathnote.libc.symbols[sym]
		elif isinstance(sym, int):
			leak = leak - sym
		else:
			logger.error("Invalid symbol/offset provided")
			return

		logger.info("Libc -> %s" % hex(leak))
		return leak

def intlibcleak(sym=0,length=14):

	if dn3_libc_exists(deathnote):

		leak = intleak(length)
		if isinstance(sym, str):
			leak = leak - deathnote.libc.symbols[sym]
		elif isinstance(sym, int):
			leak = leak - sym
		else:
			logger.error("Invalid symbol/offset provided")
			return

		logger.info("Libc -> %s" % hex(leak))
		return leak

def unhexdump(name,delim):

	if dn3_exists(deathnote):

		data = reu(delim)
		f = open("/tmp/raw_hex","w+")
		f.write(data)
		f.close()
		os.system(f"xxd -r /tmp/raw_hex > {name}", cwd=os.gewcwd())
		exe = ELF(name)
		context.binary = exe
		deathnote.binary = exe
		return exe