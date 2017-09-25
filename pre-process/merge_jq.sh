echo '' > posts2m.csv
for i in `echo *.csv`; do
    echo $i
    cat $i >>  posts2m.csv
done
