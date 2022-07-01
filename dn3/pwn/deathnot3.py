from pwn import *
from dn3.misc.encoding import *
from dn3.misc.utils import *
from dn3.config import *
from logging import getLogger
import os

logger = getLogger(__name__)

deathnote = None

class DeathNot3():

	def __init__(self,io,libc=None):

		global deathnote

		if context.binary == None:
			logger.warn("(context.binary) has not been set")

		if type(io) != pwnlib.tubes.process.process and type(io) != pwnlib.tubes.remote.remote:
			logger.error("Tube provided isn't a pwnlib process")

		if libc != None and type(libc) != pwnlib.elf.elf.ELF:
			logger.warn("Provided libc isn't a pwnlib ELF")

		self.binary = context.binary
		self.io = io
		self.libc = libc
		deathnote = self

		logger.info("deathnot3 has been initialized!")

def gdbserver(path,gdbscript=None,aslr=False):
	if gdbscript == None:
		gdbscript = ""
	f = open(gdbscript_loc,"w+")
	f.write(gdbscript)
	f.close()

	aslr = ""
	if aslr:
		aslr = "--no-disable-randomization "
	
	ctx = context.log_level
	context.log_level = "INFO"
	io = process(f"gdbserver {aslr}localhost:{gdbserver_port} {path}".split(" "))

	for i in range(3):
		io.recvline()
	context.log_level = ctx
	logger.info("GDB attached!")
	return io


def rec(n):
	if dn3_exists(deathnote):
		return bytes2str(deathnote.io.recv(n))

def reu(s):
	if dn3_exists(deathnote):
		return bytes2str(deathnote.io.recvuntil(str2bytes(s)))

def rl():
	if dn3_exists(deathnote):
		return bytes2str(deathnote.io.recvline())

def s(s):
	if dn3_exists(deathnote):
		if type(s) == str:
			return deathnote.io.send(str2bytes(s))
		elif type(s) == bytes:
			return deathnote.io.send(s)
		elif type(s) == int or type(s) == float:
			return deathnote.io.send(str2bytes(str(s)))
		else:
			logger.error(f"Expected string/int/float/bytes, got {type(s)}")

def sl(s):
	if dn3_exists(deathnote):
		if type(s) == str:
			return deathnote.io.sendline(str2bytes(s))
		elif type(s) == bytes:
			return deathnote.io.sendline(s)
		elif type(s) == int or type(s) == float:
			return deathnote.io.sendline(str2bytes(str(s)))
		else:
			logger.error(f"Expected string/int/float/bytes, got {type(s)}")

def sa(d,s):
	if dn3_exists(deathnote):
		if type(s) == str:
			return deathnote.io.sendafter(str2bytes(d),str2bytes(s))
		elif type(s) == bytes:
			return deathnote.io.sendafter(str2bytes(d),s)
		elif type(s) == int or type(s) == float:
			return deathnote.io.sendafter(str2bytes(d),str2bytes(str(s)))
		else:
			logger.error(f"Expected string/int/float/bytes, got {type(s)}")

def sla(d,s):
	if dn3_exists(deathnote):
		if type(s) == str:
			return deathnote.io.sendlineafter(str2bytes(d),str2bytes(s))
		elif type(s) == bytes:
			return deathnote.io.sendlineafter(str2bytes(d),s)
		elif type(s) == int or type(s) == float:
			return deathnote.io.sendlineafter(str2bytes(d),str2bytes(str(s)))
		else:
			logger.error(f"Expected string/int/float/bytes, got {type(s)}")

def interactive():
	global deathnote
	if dn3_exists(deathnote):
		deathnote.io.interactive()
		deathnote = None
		return

def intleak(length=14):
	return int(deathnote.io.recv(length),16)

def byteleak(length=6):
	return unpack(deathnote.io.recv(length),length*8)


def libcleak(sym=0,length=6):

	if dn3_libc_exists(deathnote):

		leak = byteleak(length)
		if type(sym) == str:
			leak = leak - deathnote.libc.symbols[sym]
		elif type(sym) == int:
			leak = leak - sym
		else:
			logger.error("Invalid symbol/offset provided")
			return

		logger.info("Libc -> %s" % hex(leak))
		return leak

def intlibcleak(sym=0,length=14):

	if dn3_libc_exists(deathnote):

		leak = intleak(length)
		if type(sym) == str:
			leak = leak - deathnote.libc.symbols[sym]
		elif type(sym) == int:
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

def dn3loop():

	if dn3_exists(deathnote):
	
		try:
			deathnote.io.unrecv(deathnote.io.recv(1))
			deathnote.io.interactive()
		except:
			return True