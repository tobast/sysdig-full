#!/bin/bash
#exec python3 clock/quartz.py init | processor/processor clock/clock.bin | display_gui/display_gui 
exec clock/quartz | processor/processor clock/clock.bin | display_gui/display_gui 
