CAS=../assembler/cas
CLOCKS=clock.bin clock_wait.bin
QUARTZ=quartz
QUARTZ0=quartz0
CC=gcc
CFLAGS=-std=c99 -O2

all: $(CLOCKS) $(QUARTZ) $(QUARTZ0)

$(QUARTZ): $(QUARTZ).c
	$(CC) $(CFLAGS) $< -o $@ 
$(QUARTZ0): $(QUARTZ0).c
	$(CC) $(CFLAGS) $< -o $@ 

%.bin: %.s
	$(CAS) $<

clean:
	rm -f $(CLOCKS) $(QUARTZ) $(QUARTZ0)
	
