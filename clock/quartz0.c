#include <stdio.h>

void print_int64(unsigned long long int val) {
	for(int byte=7; byte >=0; byte--)
		putchar((char)(val >> (byte*8)));
}

int main() {
	print_int64(0);
	print_int64(0);
	print_int64(0);
	print_int64(1);
	print_int64(1);
	print_int64(0);
	print_int64(0);

	while(1) {
		putchar(0);
		putchar(0);
		putchar(0);
		putchar(0);
		putchar(0);
		putchar(0);
		putchar(0);
		putchar(0);
		putchar(0);
		putchar(0);
		putchar(0);
		putchar(0);
		putchar(0);
		putchar(0);
		putchar(0);
		putchar(0);
	}

	return 0;
}

