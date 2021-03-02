#!/bin/bash
SCALEFACTORS=$(cat scalefactors.txt)

# running from 'amorphous' directory

for sf in ${SCALEFACTORS[@]}; do
	for i in {1..10}; do
		j=$(($i*10000))
		DIRNAME="$sf"_"$1"_"$j"
		cd deform_"$sf"_"$1"/cool_"$DIRNAME"
		cp ../../SUBMISSIONSCRIPT_COUNT.sh ./count_"$DIRNAME".sh
		qsub count_"$DIRNAME".sh
		cd ../../
	done
done
