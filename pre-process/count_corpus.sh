#!/bin/bash

#for i in `seq 0 9`;
#do


for j in `seq 2 9`;
do

echo "Processing: X$j"

python3 count_corpus.py X$j

echo "Done $j"

done
#done
