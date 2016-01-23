CAS=../assembler/cas
CLOCKS=clock.bin clock_wait.bin
QUARTZ=quartz

all: $(CLOCKS) $(QUARTZ)

$(QUARTZ): $(QUARTZ).c
	gcc -std=c99 -O2 $< -o $@ 

%.bin: %.s
	$(CAS) $<

clean:
	rm -f $(CLOCKS) $(QUARTZ)
	
