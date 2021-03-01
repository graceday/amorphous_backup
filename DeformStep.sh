#!/bin/bash
SCALEFACTORS=$(cat scalefactors.txt)
for sf in ${SCALEFACTORS[@]}; do
	DIRNAME=deform_"$sf"_"$1"
	mkdir -p "$DIRNAME"
	cp restart.melt ./"$DIRNAME"/
	cp SUBMISSIONSCRIPT.sh ./"$DIRNAME"/
	python write_scaled_input_file.py --factor "$sf" --pot "$1"
	cd "$DIRNAME"
	qsub SUBMISSIONSCRIPT.sh "$DIRNAME"
	cd ../
done
