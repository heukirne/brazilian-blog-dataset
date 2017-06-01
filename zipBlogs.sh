echo 'Uncompressing Gzipped Tar file'
#pv blogs.tar.gz | gunzip > blogs.tar
echo 'Updating Tar file'
tar -uf - ./blogs/ | pv > blogs.tar
echo 'Compressing Tar file'
pv blogs.tar | gzip > blog.tar.gz
# tar -zcvf posts.csv.gz posts.csv
echo 'Done'