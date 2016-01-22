CAS=../assembler/cas
CLOCKS=clock.bin clock_wait.bin

all: $(CLOCKS)

%.bin: %.s
	$(CAS) $<

clean:
	rm -f $(CLOCKS)
	
