CMX=ast.cmx parser.cmx lexer.cmx binary_gen.cmx linker.cmx write_rom.cmx \
	main.cmx
OBJS=ast.cmx parser.ml parser.cmx lexer.ml lexer.cmx binary_gen.cmx \
	linker.cmx write_rom.cmx main.cmx
GENERATED=lexer.ml parser.ml parser.mli
BIN=cas
FLAGS=
CMP=ocamlopt

all: $(BIN)

$(BIN): $(OBJS)
	$(CMP) $(FLAGS) -o $(BIN) $(CMX)

%.cmx: %.ml
	if [ -f $<i ] ; then $(CMP) $(FLAGS) -c $<i ; fi
	$(CMP) $(FLAGS) -c $<

parser.ml: parser.mly
	menhir --infer -v $<

lexer.ml: lexer.mll
	ocamllex $<

clean:
	rm -f *{.cmi,.cmx,.o,~} \
		$(GENERATED) \
		parser.automaton ${BIN}
