PY=python3
TARGET=processor
NETLIST=processor.net
MAIN=main.py
COMP=../simulator/compiler.native
COMPFLAGS=-iomode 2

all: $(TARGET)

$(TARGET): $(NETLIST)
	$(COMP) $(COMPFLAGS) $<

$(NETLIST): $(MAIN)
	$(PY) $< > $@

clean:
	rm -f $(TARGET) $(NETLIST) $(TARGET).c
	rm -rf __pycache__
