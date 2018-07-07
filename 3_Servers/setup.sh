#!/bin/bash
cd table_generation
./generate.sh
cd ..
OUTPUTDIR="./table_generation/output/"$(ls -t ./table_generation/output | head -1)
arr=( "a" "b" "c" )
for i in "${arr[@]}"
do
	cp -r "$OUTPUTDIR/server_$i" "./bin/server_$i/"
	rm -rf "./bin/server_$i/tables"
	mv "./bin/server_$i/server_$i" "./bin/server_$i/tables"
	cp ./src/* "./bin/server_$i/."
done
