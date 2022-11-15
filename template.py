#!/usr/bin/env python3
from dn3 import *
from pwn import ELF, asm, disasm

exe = ELF("BINARY")
l{
libc = ELF("LIBC")
}l
context.binary = exe
context.terminal = "tmux new-window".split()
#context.log = 0
#context.aslr = False

global io
breakpoints = '''
break main
'''+"continue\n"*1

r{host, port = "IP",PORT

if len(sys.argv) > 1 and sys.argv[1] == "-r":
    io = remote(host,port)
el}rif len(sys.argv) > 1 and sys.argv[1] == "-ng":
    io = process(exe.path)
else:
    io = debug(exe.path, gdbscript=breakpoints)
    
DeathNot3(io)

interactive()