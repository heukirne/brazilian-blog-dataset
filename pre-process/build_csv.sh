#!/bin/bash

#for i in `seq 0 9`;
#do


for j in `seq 0 9`;
do

pathname="./blogs/tier-X/blogs/tier-X/"$j"*/posts"

echo "Processing: $pathname"

find $pathname -name '*.json' -exec cat {} \; |
        jq -r '[.id, .blog.id, .published, .title, .content, .author.id, .author.displayName, .replies.totalItems, 
        (if .labels != null then ( .labels | join(",")) else "" end) ] 
        | @csv' | sed -e 's/<[a-zA-Z\/][^>]*>//g' > jq_posts/posts_X$j.csv

echo "Done X$j"

done
#done
