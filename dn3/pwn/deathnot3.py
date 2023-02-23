from pwn import ELF
from dn3.misc.encoding import *
from dn3.misc.utils import *
from dn3.l1ght.context import ctx
from logging import getLogger
import os

logger = getLogger(__name__)

deathnote = None

class DeathNot3():

	def __init__(self,io=None,libc=None):

		global deathnote

		if io == None:
			io = ctx.io

		if libc == None:
			libc = ctx.libc

		if ctx.binary == None:
			logger.warn("(ctx.binary) has not been set")

		if not set(["recv","recvline","recvuntil","send","sendline","sendafter","sendlineafter","interactive"]).issubset(set(io.__dir__())):
			logger.error("Pipe isn't supported")

		if libc and not isinstance(libc, ELF):
			logger.error("Provided libc isn't a pwnlib ELF")

		self.binary = ctx.binary
		self.io = io
		self.libc = libc
		deathnote = self

		logger.info("deathnot3 has been initialized!")


def re(n):
	if dn3_exists(deathnote):
		return x2sb(deathnote.io.recv(n),ctx.mode)

def reu(s):
	if dn3_exists(deathnote):
		return x2sb(deathnote.io.recvuntil(x2sb(s,ctx.mode)),ctx.mode)

def rl():
	if dn3_exists(deathnote):
		return x2sb(deathnote.io.recvline(),ctx.mode)

def s(s):
	if dn3_exists(deathnote):
		return deathnote.io.send(x2sb(s,ctx.mode))

def sl(s):
	if dn3_exists(deathnote):
		return deathnote.io.sendline(x2sb(s,ctx.mode))

def sa(d,s):
	if dn3_exists(deathnote):
		return deathnote.io.sendafter(x2sb(d,ctx.mode),x2sb(s,ctx.mode))

def sla(d,s):
	if dn3_exists(deathnote):
		return deathnote.io.sendlineafter(x2sb(d,ctx.mode),x2sb(s,ctx.mode))

def shell():
	global deathnote
	if dn3_exists(deathnote):
		deathnote.io.interactive()
		deathnote = None
		return

def intleak(length=14):
	return int(x2str(deathnote.io.recv(length)),16)

def byteleak(length=6):
	if length > 8:
		logger.error("Maximum leak size can only be 8 bytes!")
	return upk(deathnote.io.recv(length))


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
		ctx.binary = exe
		deathnote.binary = exe
		return exe