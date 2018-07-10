#!/bin/sh
echo "Generating tables"
python generate.py
echo "Rotating tables"
OUTPUTDIR="./output/"$(ls -t ./output | head -1)

arr=( "a" "b" "c" "d" "e" "f" )
for i in "${arr[@]}"
do
	mv "$OUTPUTDIR/server_$i/result.lut" "$i""_result.lut"
done

mv "a_result.lut" "$OUTPUTDIR/server_b/result.lut"
mv "b_result.lut" "$OUTPUTDIR/server_c/result.lut"
mv "c_result.lut" "$OUTPUTDIR/server_d/result.lut"
mv "d_result.lut" "$OUTPUTDIR/server_e/result.lut"
mv "e_result.lut" "$OUTPUTDIR/server_f/result.lut"
mv "f_result.lut" "$OUTPUTDIR/server_a/result.lut"

echo "Tables are at $OUTPUTDIR"
