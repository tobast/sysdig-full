# sysdig
Simulation of a processor, its circuit, its assembly and a program in it using net-list for the L3 class project &lt;http://www.di.ens.fr/~bourke/sysdig.html&gt;

Goals
===

This project aims to provide four components:

* A net-list to C(++) compiler, in order to be as optimized as possible, allowing the user to compile their net-list files with any C(++) compiler (eg. g++/gcc) to achieve high performance. In this particular context, the goal is to compile the net-list of a processor;

* the net-list code for a full processor with a given instruction set (to be defined); 

* an assembler for this processor;

* and a program of real-time clock for this processor.

Optionnaly, we might choose later to include an alternative program to Minijazz, generating net-list code from a higher level language (especially including functions).
