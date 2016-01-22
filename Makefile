###################################################################
#### Meta-Makefile ################################################
# Compiles every component of the digital clock separately and    #
# easily.                                                         #
###################################################################

DIR_LIST=display_gui assembler clock simulator processor
QMAKE=qmake-qt5
MAKE=make

all: display_gui_mkf
	for dir in $(DIR_LIST); do $(MAKE) -C $$dir ; done

display_gui_mkf:
	(cd display_gui && $(QMAKE))

assembler:
	$(MAKE) -C $@
clock: assembler
	$(MAKE) -C $@
display_gui: display_gui_mkf
	$(MAKE) -C $@
simulator:
	$(MAKE) -C $@
processor:
	$(MAKE) -C $@



clean: display_gui_mkf
	@for dir in $(DIR_LIST); do $(MAKE) -C $$dir clean; done
	rm display_gui/display_gui # Not cleaned by Qt by default


run: all
	bash ./run_realtime.sh

run-fast: all
	bash ./run_fast.sh

run-very-fast: all
	bash ./run_very_fast
