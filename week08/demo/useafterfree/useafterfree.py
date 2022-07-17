from pwn import *

context.arch = 'i386'
context.terminal = ['urxvt', '-e', 'sh', '-c']
context.log_level = 'error'

p = gdb.debug('./useafterfree') 

p.interactive()
p.close()