#!/usr/bin/bash

while true; do
	date | tr -d '\n'
	echo -ne '\r'
	sleep 0.01
done
