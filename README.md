DeathNot3
===
<p align="center">
   <img src="https://media.discordapp.net/attachments/1015263562668720150/1078325086307766344/dn3_logo.png" height=256 width=256/>
</p>

[![pypi](https://img.shields.io/pypi/v/dn3?style=for-the-badge)](https://pypi.org/project/dn3/)
![python-version](https://img.shields.io/pypi/pyversions/dn3?style=for-the-badge)
![last-commit](https://img.shields.io/github/last-commit/k1R4/deathnot3/dev?style=for-the-badge)
![build-status](https://img.shields.io/github/actions/workflow/status/k1R4/deathnot3/python-package.yml?style=for-the-badge)
![license](https://img.shields.io/pypi/l/dn3?style=for-the-badge)
[![twitter](https://img.shields.io/twitter/follow/justk1R4?style=for-the-badge)](https://twitter.com/justk1R4)

## Installation
```
sudo apt-get update
sudo apt-get install python3 python3-pip
python3 -m pip install --upgrade dn3
```

## Description
DeathNot3 is a one-for-all, all-for-one tool that aims to make solving CTF pwn challenges easier and faster. 

deathnot3 was started as a wrapper for pwntools, but with the addition of the "l1ght" submodule, it has become a lightweight alternative to pwntools process/remote
while providing additional functionality.
deathnot3 aims to:
 - allow strings and bytes interchageably
 - be lightweight
 - provide basic automation
 - be an all around pwn helper for CTFs

## Requirements
Supports: Python 3.6+

Library Dependency:
- pyelftools
- zstandard
- unix_ar
- requests
- wget

## Usage

 ```py
  from dn3 import *

  binary = ELF("./binary")
  libc = ELF("./libc.so.6")

  ctx.mode = str 
  ctx.libc = libc     
  # recv in string. Can also be set to bytes
  
  io = process("./binary")
  DeathNot3()              # Initialize deathnot3
  
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
	 - edit config using `dn3 cfg` and specify template format url or path (if path prefix with `local:`)
	 - [example template format](https://raw.githubusercontent.com/k1R4/deathnot3/dev/template.py)
	 
	**`dn3 linker <binary_path> -l <libc_path>`**
	 - Find appropriate dynamic linker for given libc and patch binary with it and provided libc using `patchelf`

   **`dn3 cfg <key(optional)>`**
    - Edit dn3's config
    - config is located at `~/.dn3.conf`

## TODO
 - [x] Implement ELF similar to that of pwntools
 - [ ] Add inline description comments for code
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