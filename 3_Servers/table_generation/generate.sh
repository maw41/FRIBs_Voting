#!/bin/sh
echo "Generating tables"
python generate.py
echo "Rotating tables"
OUTPUTDIR="./output/"$(ls -t ./output | head -1)

mv "$OUTPUTDIR/server_a/result.lut" "a_result.lut"
mv "$OUTPUTDIR/server_b/result.lut" "b_result.lut"
mv "$OUTPUTDIR/server_c/result.lut" "c_result.lut"
mv "a_result.lut" "$OUTPUTDIR/server_b/result.lut"
mv "b_result.lut" "$OUTPUTDIR/server_c/result.lut"
mv "c_result.lut" "$OUTPUTDIR/server_a/result.lut"


echo "Tables are at $OUTPUTDIR"
