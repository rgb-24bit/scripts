#!/bin/bash
#
# Convert subfiles and subfolder names in the current directory to lowercase.

for fn in *; do
    lfn=`echo $fn | tr 'A-Z' 'a-z'`
    echo $lfn
    [ "$fn" != "$lfn" ] && mv ./"$fn" ./"$lfn"
done

