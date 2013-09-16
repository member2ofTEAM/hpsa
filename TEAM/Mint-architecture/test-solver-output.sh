#!/bin/bash
echo Team $(expr $RANDOM % 32)
echo -n '1 '
for i in $(seq 1 4)
do
	echo -n "$(expr $RANDOM % 100)"
	if [ $i -ne 4 ]; then
		echo -n ' '
	fi
done
echo
