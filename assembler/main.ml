open Lexing
open Format

let usage = "usage: cas [options] file.s"

let rec spec =
  [
	"-h", Arg.Unit (fun () -> Arg.usage spec usage; exit 0),
	  "  Display this list of options";
  ]

let file =
  let file = ref None in
  let set_file s =
    if not (Filename.check_suffix s ".s") then
      raise (Arg.Bad "Input file should have a .s extension");
    file := Some s
  in
  Arg.parse spec set_file usage;
  match !file with Some f -> f | None ->
	 Arg.usage spec usage; exit 1

let escape_string ff s =
  for i = 0 to String.length s - 1 do
	match s.[i] with
	| '"' -> fprintf ff "\\\""
	| '\\' -> fprintf ff "\\\\"
	| _ -> fprintf ff "%c" s.[i]
  done

let report_error filename start_pos end_pos =
  let start_col = start_pos.pos_cnum - start_pos.pos_bol + 1 in
  let end_col = end_pos.pos_cnum - start_pos.pos_bol + 1 in
  eprintf "File \"%a\", line %d, characters %d-%d:\n" escape_string filename start_pos.pos_lnum start_col end_col

let in_chan = open_in file
let lexbuf = Lexing.from_channel in_chan
let prog =
  try
	Parser.prgm Lexer.token lexbuf
  with
  | Lexer.Lexical_error s ->
	 begin
	   report_error file (lexeme_start_p lexbuf) (lexeme_end_p lexbuf);
	   eprintf "%s@." s; exit 1
	 end
  | Parser.Error ->
	 begin
	   report_error file (lexeme_start_p lexbuf) (lexeme_end_p lexbuf);
	   eprintf "Syntax error@."; exit 1
	 end

let prog = Linker.link prog
let opcodes = Binary_gen.binary_gen prog
let rom_filename = (Filename.chop_suffix file ".s") ^ ".bin"
let out_file = open_out rom_filename
let () = Write_rom.print_rom out_file opcodes
let () = close_out out_file
let () = exit 0
