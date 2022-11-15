deathnot3
====

## Description
deathnot3 was created as a wrapper for pwntools, but with the addition of the "l1ght" submodule, it aims to be a lightweight alternative to pwntools
while providing majority of the essential functionality for exploit scripts.
deathnot3 aims to:
 - allow strings and bytes interchageably
 - be lightweight
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

  binary = ELF("./binary")
  libc = ELF("./libc.so.6")

  context.mode = str      
  # recv in string. Can also be set to bytes
  
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
	 - edit config using `dn3 config` and specify template format url or path (if path prefix with `local:`)
	 - [example template format](https://raw.githubusercontent.com/k1R4/deathnot3/v1.0.0/template.py)
	 
	**`dn3 linker <binary_path> -l <libc_path>`**
	 - Find appropriate dynamic linker for given libc and patch binary with it and provided libc using `patchelf`

    **`dn3 config <key(optional)>`**
     - Edit dn3's config
     - Config is located at `~/.dn3.conf`

## TODO
 - [ ] Implement ELF similar to that of pwntools
 - [ ] Implement buffering for process, remote
 - [ ] Add automation
    - [ ] static vulnerability detection
    - [ ] ret2win
    - [ ] ret2shellcode
    - [ ] ret2libc/ROP
    - [ ] tcache poisoning
 - [ ] Add documentation to wiki
 - [ ] Add support for big endian
 - [ ] Add support for arm based architectures
    - [ ] aarch64
    - [ ] arm