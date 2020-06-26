import random

key = b'g1mm3fl4g_plz'
keylen = len(key)

code = b'\x55\x48\x89\xe5\x48\x83\xec\x20\x48\x89\x7d\xe8'
# code += b'\x8b\x05\xbb\x0a\x20\x00'
code += b'\x8b\x05\xb6\x00\x00\x00'   # mov eax, isPtraced
code += b'\x85\xc0\x75\x24\xb9\x00\x00\x00\x00\xba\x01\x00\x00\x00\xbe\x00\x00\x00\x00\xbf\x00\x00\x00\x00\xb8\x00\x00\x00\x00'
# code += b'\xe8\xd5\xfe\xff\xff'
code += b'\xe8\x6c\xf3\xdf\xff'       # call ptrace
# code += b'\x89\x05\x93\x0a\x20\x00' 
code += b'\x89\x05\x8e\x00\x00\x00'   # mov DWORD PTR isPtraced, eax  
# code += b'\x8b\x05\x8d\x0a\x20\x00'
code += b'\x8b\x05\x88\x00\x00\x00'   # mov eax, DWORD PTR isPtraced
code += b'\x83\xf8\xff\x75\x0e'
# code += b'\x48\x8d\x3d\x3d\x01\x00\x00'
code += b'\x48\xC7\xC7\x98\x11\x60\x00'   # mov rdi, "Get out!"
# code += b'\xe8\xa8\xfe\xff\xff'
code += b'\xe8\x3f\xf3\xdf\xff'       # call puts
code += b'\xeb\x5d\x48\x8b\x45\xe8\x48\x83\xc0\x0d\x0f\xb6\x00\x3c\x21\x75\x4e\xc7\x45\xfc\x00\x00\x00\x00\xeb\x35\x8b\x45\xfc\x83\xc0\x0a\x48\x63\xd0'
# code += b'\x48\x8d\x05\x2e\x01\x00\x00'
code += b'\x48\xC7\xC0\x80\x10\x60\x00'    # mov rax, flag_enc
code += b'\x0f\xb6\x0c\x02\x8b\x45\xfc\x48\x63\xd0'
# code += b'\x48\x8d\x05\x5d\x01\x00\x00' 
code += b'\x48\xC7\xC0\x60\x10\x60\x00'    # mov rax, flag_key
code += b'\x0f\xb6\x04\x02\x31\xc8\x0f\xbe\xc0\x89\xc7'
# code += b'\xe8\x4d\xfe\xff\xff'       
code += b'\xe8\xe4\xf2\xdf\xff'       # call putchar 1
code += b'\x83\x45\xfc\x01\x83\x7d\xfc\x1e\x7e\xc5\xbf\x0a\x00\x00\x00'
# code += b'\xe8\x39\xfe\xff\xff'       
code += b'\xe8\xd0\xf2\xdf\xff'       # call putchar 2
code += b'\x90\xc9\xc3'

print(f'code length: {len(code)}\ncode:\n{code.hex(" ")}')



factor = b'\x7e\x49\x7f\xc0\x1c\xe0\xd2\xf1\x4c\x4d\x4f\x74\xf0'
iv = b'\x95\xad\xd4\xfe\x77\x5f\x6f\xae\xea\x78\x82\x60\x47'

assert keylen == len(factor)
assert len(factor) == len(iv)


# password encryption
ciphered = b''
for i, b in enumerate(key):
	ciphered += (b ^ ((iv[i] * factor[i]) & 0xff)).to_bytes(1, 'little')

should_be_pwd = b''
for i, b in enumerate(ciphered):
	should_be_pwd += (b ^ ((iv[i] * factor[i]) & 0xff)).to_bytes(1, 'little')

print(f'ciphered alpha: {ciphered}\nciphered: {ciphered.hex(" ")}\npwd: {should_be_pwd}\n')


# code encrytpion
ciphered = b''
for i, b in enumerate(code):
	ciphered += (key[i % keylen] ^ code[i]).to_bytes(1, 'little')

should_be_key = b''
for i, b in enumerate(ciphered):
	should_be_key += (b ^ code[i]).to_bytes(1, 'little')

print(f'code ciphered (EASY):\n{ciphered.hex(" ")}\nkey: {should_be_key}\n')


# flag encryption
flag = b'flag{nice_little_rev_my_friend}'
onetime_key = b''
for i in range(len(flag)):
	onetime_key += random.randint(0, 255).to_bytes(1, 'little')
print(f'flag: {flag}\nkey: {onetime_key.hex(" ")}')

ciphered = b''
for i, b in enumerate(flag):
	ciphered += (b ^ onetime_key[i]).to_bytes(1, 'little')

should_be_flag = b''
for i, b in enumerate(ciphered):
	should_be_flag += (b ^ onetime_key[i]).to_bytes(1, 'little')

print(f'ciphered: {ciphered.hex(" ")}\nflag: {should_be_flag}\n')



# # code encryption (CON FATTORE)
# ciphered = b''
# for i, b in enumerate(code):
# 	ciphered += (key[i % keylen] ^ ((code[i] * factor[i % keylen]) & 0xff)).to_bytes(1, 'little')

# should_be_key = b''
# for i, b in enumerate(ciphered):
# 	should_be_key += (b ^ ((code[i] * factor[i % keylen]) & 0xff)).to_bytes(1, 'little')

# print(f'ciphered alpha: {ciphered}\ncode ciphered (HARD): {ciphered.hex(" ")}\nkey: {should_be_key}\n')
