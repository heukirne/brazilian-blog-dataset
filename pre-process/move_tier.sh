#!/bin/bash

for i in `seq 1 9`;
do

	pathto="./blogs/tier-"$i"/"


	for j in `seq 0 9`;
	do

	pathfrom="./blogs/"$i$j"*"
	

	echo "Processing: $pathfrom to $pathto"

	mv $pathfrom $pathto

	echo "Done $i"

	done

done
