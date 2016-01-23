#!/bin/bash

# Same as run_fast, but starts from 00:00:00 01-01-0000, which is
# easier to benchmark.

exec clock/quartz0 | processor/processor clock/clock.bin | display_gui/display_gui 
