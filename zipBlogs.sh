echo 'Delete empty directories'
#find ./blogs/ -type d -empty -delete | pv
#echo 'Uncompressing Gzipped Tar file'
#pv blogs.tar.gz | gunzip > blogs.tar
echo 'Create new Tar file'
tar -cf - ./blogs/ | pv > blogs.tar
echo 'Compressing Tar file'
pv blogs.tar | gzip > blogs.tar.gz
# tar -zcvf posts.csv.gz posts.csv
echo 'Done'
