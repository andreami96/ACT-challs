from pwn import *

# elf addresses
PTRACE_PLT = 0x400480
PUTS_PLT = 0x400470
PUTCHAR_PLT = 0x400460

code = 0x6010e0
isPtraced = 0x6011a8
getOut = 0x601198
flag_enc = 0x601080
flag_key = 0x601060

# IP after calls of part2
next_rip_ptrace = 0x4005ab
next_rip_puts = 0x4005c8
next_rip_putchar_1 = 0x400613
next_rip_putchar_2 = 0x400627
next_rip_isPtraced_1 = 0x400589
next_rip_isPtraced_2 = 0x4005b1
next_rip_isPtraced_3 = 0x4005b7


OFFS_ptrace_call = -(0x6010e0 + (next_rip_ptrace - 0x400577) - PTRACE_PLT)
OFFS_puts_call = -(0x6010e0 + (next_rip_puts - 0x400577) - PUTS_PLT)
OFFS_putchar_call_1 = -(0x6010e0 + (next_rip_putchar_1 - 0x400577) - PUTCHAR_PLT)
OFFS_putchar_call_2 = -(0x6010e0 + (next_rip_putchar_2 - 0x400577) - PUTCHAR_PLT)
OFFS_isPtraced_1 = -(0x6010e0 + (next_rip_isPtraced_1 - 0x400577) - isPtraced)
OFFS_isPtraced_2 = -(0x6010e0 + (next_rip_isPtraced_2 - 0x400577) - isPtraced)
OFFS_isPtraced_3 = -(0x6010e0 + (next_rip_isPtraced_3 - 0x400577) - isPtraced)

def my_unsigned(bits, value):
	if value < 0:
		value = ( 1<<bits ) + value
	if bits == 32:
		return p32(value).hex()
	elif bits == 64:
		return p64(value).hex()


print(f'ptrace: {my_unsigned(32, OFFS_ptrace_call)}')
print(f'puts: {my_unsigned(32, OFFS_puts_call)}')
print(f'putchar 1: {my_unsigned(32, OFFS_putchar_call_1)}')
print(f'putchar 2: {my_unsigned(32, OFFS_putchar_call_2)}')
print(f'isPtraced 1: {my_unsigned(32, OFFS_isPtraced_1)}')
print(f'isPtraced 2: {my_unsigned(32, OFFS_isPtraced_2)}')
print(f'isPtraced 3: {my_unsigned(32, OFFS_isPtraced_3)}')

# OUTPUT
# ptrace: bcf3dfff
# puts: 7ff3dfff
# putchar 1: 24f3dfff
# putchar 2: 10f3dfff
# isPtraced 1: a6000000
# isPtraced 2: 7e000000
# isPtraced 3: 78000000





