from pwn import *

context.arch = 'i386'
context.terminal = ['urxvt', '-e', 'sh', '-c']
context.log_level = 'error'

p = gdb.debug('./doublefree') 

p.interactive()
p.close()