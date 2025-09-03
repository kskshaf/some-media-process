#!/usr/bin/bash

mkdir -p 10924/used
mkdir -p 10925/used
flac_cus="/home/rip/ripenv/bin/flac"

cd 10924
for i in `find ./* -name '*.wav'`; do
    $flac_cus -8 -j 16 $i
    mv $i used/
done

cd ../10925
for i in `find ./* -name '*.wav'`; do
    $flac_cus -8 -j 16 $i
    mv $i used/
done
