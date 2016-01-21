#!/bin/bash
exec python3 clock/quartz.py | processor/processor clock/clock_wait.bin | display_gui/display_gui 