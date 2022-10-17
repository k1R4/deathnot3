deathnot3
====

## Description
deathnot3 was created as a wrapper for pwntools, but with the addition of the "l1ght" submodule, it aims to be a more lightweight alternative to pwntools
while providing majority of the essential functionality.
deathnot3 aims to:
 - allow strings and bytes interchageably
 - be more lightweight
 - provide basic automation
 - be an all around pwn helper for CTFs

## Requirements
Supports: Python 3.6+

Library Dependency:
- pwntools
- zstandard
- unix_ar
- requests
- wget

## Usage

 ```py
  from dn3 import *
  from pwn import ELF

  libc = ELF("./libc.so.6")
  io = process("./binary")
  DeathNot3(io, libc=libc) # Initialize deathnot3
  
  reu("yeet")              # equivalent of io.recvuntil()
  sl(b"leet")              # equivalent of io.sendline()
  sla("yeet",8)            # equivalent of io.sendlineafter()
  s("bruh")                # equivalent of io.send()
  # bytes, string and integers can be used interchageably to send
  
  sl(p64(0xdeadbeef))      # equivalent of p64() but returns string
  sla("oof", flat([
	  0xdeadbeef,"ABCD"    # equivalent of flat() but returns string
	  ])
  
  libc = libcleak("puts")  # Offset integer can be given instead of symbol
  # Equivalent to
  # libc = unpack(io.recv(6),48) - libc.symbols.puts
  # log.info("Libc -> %s" % hex(libc)
  
  interactive()             # equivalent of io.interactive()
  ```

 - CLI
 
	**`dn3 template <binary_path> -l <libc_path> -r <ip>:<port>`**
	- used to generate template exploit on the go, based on a template format
	 - edit config at root of installation, typically at `~/.local/lib/python3.x/site-packages/dn3/config.py` and specify template format url or path (if path prefix with `local:`)
	 - [example template format](https://github.com/k1R4/Pwn/blob/main/dn3_template.py)
	 
	**`dn3 linker <binary_path> -l <libc_path>`**
	 - Find appropriate dynamic linker (ld-linux-x86-64.so.2) for given libc and patch binary with it and provided libc using `patchelf`
