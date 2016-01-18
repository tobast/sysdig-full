
let print_bytes out l =
  List.iter (output_byte out) l

let int64_to_bytes n =
  Int64.(
	[to_int (logand 255L (shift_right n 56));
	 to_int (logand 255L (shift_right n 48));
	 to_int (logand 255L (shift_right n 40));
	 to_int (logand 255L (shift_right n 32));
	 to_int (logand 255L (shift_right n 24));
	 to_int (logand 255L (shift_right n 16));
	 to_int (logand 255L (shift_right n  8));
	 to_int (logand 255L (            n   ))])

let rom_size = 1 lsl 16

let print_rom out l =
  List.iter (fun n -> print_bytes out (int64_to_bytes n)) l;
  for i = 1 to rom_size - (List.length l) do
    print_bytes out (int64_to_bytes 0L)
  done
