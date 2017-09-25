#!/bin/bash

for i in `seq 0 9`;
do


for j in `seq 0 9`;
do

pathname="./blogs/tier-"$i"/"$i$j"*/posts"

echo "Processing: $pathname"

find $pathname -name '*.json' -exec cat {} \; |
        jq -r '[(if .labels != null then ( .labels | join(",")) else "" end) ] 
        | @csv' | sed -e 's/\"//g' | sed -e 's/,/\n/g' > jq_tags/tags_$i$j.csv

echo "Done $i"

done
done
