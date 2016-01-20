# Inputs/outputs -- Digital clock

7-segments
====

Each 7-segments displayer value is encoded by a byte. A bit of this byte is
set to 1 iff the corresponding segment is lit. The segments are considered in
this order:

_gfedcba

where a is the least significant bit, and the segments are as follows:

|-a-|

f   b

|-g-|

e	c

|-d-|

Words
====

A date/time data consists in two 64-bits values, that is, two words.

The time word is passed before the date word.

Time word
====

The time word consists in the following bytes (from most significant to
least significant) :

[H][H][M][M][S][S]

Date word
====

The date word consists in the following bytes (from most significant to
least significant) :

[Y][Y][Y][Y][M][M][D][D]

