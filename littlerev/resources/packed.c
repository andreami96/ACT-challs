#include <stdio.h>
#include <sys/ptrace.h>

#define OFFS_ENC 10
#define FLAG_LEN 31

int isDebugged = 0;

void fun(char* pwd) {
	int i;

	// flag{nice_little_rev_my_friend}
	static const char flag_key[] = {0x0d,0x67,0xf1,0xc6,0x98,0xd2,0xe5,0x2d,0xb4,0x3b,0xb6,0xf2,0x2c,0xb2,0xe0,0x48,0x4c,0xe3,0xad,0x3c,0xf2,0x88,0x00,0x07,0xf4,0x8c,0x63,0x54,0xd5,0x8e,0xe3};
	static const char flag_enc[] = {0xd5,0x96,0x4b,0x23,0x31,0xb4,0x3e,0x6c,0x34,0xb2,  0x6b,0x0b,0x90,0xa1,0xe3,0xbc,0x8c,0x4e,0xd1,0x64,0xda,0x9b,0x58,0xc6,0x8c,0x2d,0x13,0x91,0xc8,0x4a,0xad,0xe5,0x79,0x58,0x92,0xfe,0x0a,0x31,0xbb,0xea,0x9e,  0x29,0xf5,0x9d,0xb2,0x66,0x53,0x8a,0x0d};

	if (!isDebugged)
		isDebugged = ptrace(PTRACE_TRACEME, 0, 1, 0);
	if (isDebugged == -1) {
		puts("Get out!");
	} else {
		if (pwd[13] == '!') {
			// decipher one time pad encrypted flag
			for(i = 0; i < FLAG_LEN; i++) {
				putchar(flag_enc[OFFS_ENC + i] ^ flag_key[i]);
			}
			putchar('\n');
		}
	}

}

int main(int argc, char* argv[]){
	fun(argv[0]);
}