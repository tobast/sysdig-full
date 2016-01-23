from time import time, sleep
from datetime import datetime
from sys import argv, exit

def print_0():
	print("\0\0\0\0\0\0\0\0", end = "")
def print_1():
	print("\0\0\0\0\0\0\0\x01", end = "")

def print_int64(n):
	for i in range(0, 64, 8):
		print(chr((n >> (56 - i)) & 255), end = "")

def print_header():
	dt = datetime.now()
	print_int64(dt.second)
	print_int64(dt.minute)
	print_int64(dt.hour)
	print_int64(dt.day)
	print_int64(dt.month)
	print_int64(dt.year % 100)
	print_int64(dt.year // 100)

print_header()
if len(argv) >= 2 and argv[1] == "init":
	exit(0)
t0 = time()
while True:
	t1 = time()
	if t1 >= t0 + 1.:
		t0 += 1.
		print_1()
	else:
		print_0()
	sleep(0.0001)
