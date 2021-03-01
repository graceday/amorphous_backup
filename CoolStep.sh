#!/bin/bash
SCALEFACTORS=$(cat scalefactors.txt)

# Running from 'amorphous' directory.

for sf in ${SCALEFACTORS[@]}; do
	for i in {1..10}; do
		j=$(($i*10000))
		DIRNAME="$sf"_"$1"_"$j"
		mkdir ./deform_"$sf"_"$1"/cool_"$DIRNAME"
		python write_cooling_input_file.py --factor "$sf" --pot "$1" --step "$j"
		cd deform_"$sf"_"$1"/cool_"$DIRNAME"
		cp ../restart.deform_"$DIRNAME" ./
		cp ../../SUBMISSIONSCRIPT_COOL.sh ./cool_"$DIRNAME".sh
		qsub cool_"$DIRNAME".sh "$DIRNAME"
		cd ../../
	done
done
		
