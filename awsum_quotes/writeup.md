# awsum-quotes

The program is a collection of quotations, each composed of two strings: the actual text of the quotation and the author.

The collection is implemented as a structure which contains:

- number of stored quotations, as an integer
- array of quotations (length 8)

Each quotation is also a structure:

- text (length 80)
- author (length 30)

The main menu allows the following operations:

1. Show all the quotations
2. Show a specific quotation
3. Add a new quotation to the collection

During the inital setup, the program fills 5 out of the 8 elements available in the quotations array, so the user can add only 3 more quotations. If it tries to add more, the program will terminate. 

_Some of the default quotations may give small hints on the solution of the challenge._

## Writeup

### An unexpected gadget

`checksec` shows that the binary has all the security options in place, so some kind of ROP will probably be necessary. We run `ropper` to see if there are some useful gadgets:

<p align="center">
<img src="https://i.imgur.com/TaMjVn7.png"
     alt="gadgets"
     width="70%"/>
  </p>

Well, that's unusual: at 0x994 there is a gadget that seems to be preparing the registers for the syscall _SYS_EXECVE_. Why should the program execute those instructions? Checking with Ghidra, we see that the instructions are not recognized by the disassembler and they are not reached by any flow of execution:

<p align="center">
<img src="https://i.imgur.com/qDvVHfu.png"
     alt="nice gadget"
     width="70%"/>
  </p>

The area of code in which the gadget resides is actually _padding code_ that the compiler adds so that the beginning of some functions are aligned at nibble level (4 bits). Normally in x64 this padding code is a [_multi-byte NOP_](https://stackoverflow.com/questions/25545470/long-multi-byte-nops-commonly-understood-macros-or-other-notation) (or a sequence of them):

<p align="center">
<img src="https://i.imgur.com/f51Qt2g.png"
     alt="multi-byte NOPs"
     width="70%" align="center"/>
  </p>

In this case, the multi-byte NOP has been partially overwritten with the instructions of the gadget. That's interesting.

Let's go back to the list of gadgets and see if there is everything we need to prepare the registers for the _SYS_EXECVE_: we need to set RAX, RDI, RSI and RDX. The gadget mentioned takes care of RDI and RAX, there is another gadget that pops RSI but there is nothing for RDX. RDX will point to the environment of the execve so it can't be a random value (the easiest way is to make it a pointer to NULL), but there is no gadget that gives us control over it. 

But wait, let's think about what we saw until now: somebody put instructions that seem like a backdoor inside some padding code. Maybe there is other padding code that has been altered in the same fashion?

<p align="center">
<img src="https://i.imgur.com/1tLyJLo.png"
     alt="new part of the gadget"
     width="70%"/>
  </p>

Ha-ha! Just before the bytes of the backdoor gadget there is another strange padding sequence. Disassembling those bytes we find:

```assembly
pop rdx
mov rsi, rdx
jmp <+0x7>
```

This small block jumps to the backdoor gadget, so they are actually a single magic gadget that pops everything that is needed to call _SYS_EXECVE_. With this gadget we will only need to somehow prepare the stack with a pointer to NULL (8 null bytes) and a pointer to the string "/bin/sh". The latter can be found in _.rodata_ because it is used as the author string for one of the default quotations.

At this point we have a clear idea of what to do: find some way to hijack the flow of the program and execute the magic gadget. Let's see what vulns we can find.

### Buffer overflow

There is an evident buffer overflow in the `get_new_quote()` function, both in the text of the quotation and in the author buffers. The program calls two `read()` of 0x90 bytes for buffers of length 80 (text) and 30 (author). 

Also, the text buffer is printed to stdout before reading the the author, so... what about overflowing the buffer until we reach the canary, so that the canary itself is printed as part of the text buffer? 

#### Leaking stuff

Let's look at the stack we get before sending our input: 

<p align="center">
<img src="https://i.imgur.com/GZDDrn7.png"
     alt="stack layout"
     width="70%"/>
  </p>

Highlighted in blue and green are the beginning of the text and author buffers, respectively. 

Our end goal is to overwrite the __saved IP__ with the address of the magic gadget. Since the binary is PIE, a leak of the _.text_ section is needed in order to calculate that addres. Can we leak the saved IP? 

Yes, but it's a bit convoluted. We can't leak it directly because the __canary__ would be modified in the process; then the program would exit before returning from `get_new_quote()`. What we can do is to leak the canary first, together with the __saved BP__, and only then, leak the saved IP.

It's time to add some quotes.

#### Quote #1

_leak canary + saved BP_

The idea is to write enough bytes in the text buffer to reach the canary. We need 0x58 bytes (writing into memory goes towards the higher addresses). Since `printf` prints until the character terminator (null byte `\x00` for C programs), we need to overwrite also the least significan byte of the canary - notice that the canary is implemented so that it always has a null byte at the end.

Since the program performs a substitution of the first `\n` (newline) character in the buffer with a null byte, we must make sure that also the newline byte `\x0a` is not in our buffer.

__Can we?__ Well, the we control the payload of 0x58 + 1 bytes, so no problem for that, but don't forget that also the canary itself will be part of our buffer and we have no control on it whatsoever: it is a random number generated at the beginning of the execution. From now on we assume that the canary does not contain any newline or null characters, besides the least significant byte that is always `\x00`, as we said. We'll discuss the other case later. This reasoning applies for all the values that we will leak in this exploit. 

Together with the canary, the printf will print also the saved BP. It won't print further than that because the 2 most significant bytes of the saved BP are always `\x00`. 

After the leak, we can restore the least significant byte of the canary with the overflow of the author buffer. This time the payload will be 0x78 + 1 bytes long, with the last byte set to `\x00`. This way the program won't detect any change on the canary upon return form `get_new_quote()`.

#### Quote #2

_leak saved IP_

At this point we know the canary and the saved BP. We can leak the saved IP following the same process described for the first quote:

1. write enough bytes to reach the value to leak (text buffer overflow)
2. restore values on the stack to let the execution go on (author buffer overflow)

For the first part 0x68 bytes are needed. For the second, we must restore both the canary and the saved BP.

#### Quote #3

_final trigger_

Now we know where to jump. After finding the addresses of "/bin/sh" and of 8 `\x00` bytes in the executable, let's send everything in the text buffer _(from low to high addresses)_:

- padding bytes
- canary
- saved BP
- address of the gadget
- address of null bytes
- address of "/bin/sh"

After sending a short author string, we get the shell. 

```bash
> cat flag
```

## Issues

Throughout the exploit, we assumed that the leaked values didn't have any `\x00` or `\x0a` bytes. They are all random values: the __canary__ is random by implementation, the addresses of the stack (__saved BP__) and the .text segment (__saved IP__) are randomized by ASLR. There is nothing that can be done about that, that's why this exploit is not always succesful.

Testing 30 runs gave a success rate of _~75%_.



## Hosting

The challenge can be hosted on a system with the latest libc-2.31. The exploit does not make use of libc addresses.

Compiled with gcc 7.5.0 (Ubuntu 18.04)

```
gcc -o awsum_quotes awsum_quotes.c
```

