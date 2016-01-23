#include <stdio.h>
#include <time.h>

void print_int64(unsigned long long int val) {
	for(int byte=7; byte >=0; byte--)
		putchar((char)(val >> (byte*8)));
}

int main() {
	time_t rawTime;
	time(&rawTime);
	struct tm* curTime = localtime(&rawTime);
	curTime->tm_year += 1900;
	curTime->tm_mon ++;

	print_int64(curTime->tm_sec);
	print_int64(curTime->tm_min);
	print_int64(curTime->tm_hour);
	print_int64(curTime->tm_mday);
	print_int64(curTime->tm_mon);
	print_int64(curTime->tm_year % 100);
	print_int64(curTime->tm_year / 100);

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

