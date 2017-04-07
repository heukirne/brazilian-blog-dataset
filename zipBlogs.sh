gunzip blogs.tar.gz
tar -uvf blogs.tar ./blogs/
gzip -f blogs.tar
# tar -zcvf posts.csv.gz posts.csv
echo 'Done'
