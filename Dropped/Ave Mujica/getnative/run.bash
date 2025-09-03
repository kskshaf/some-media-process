#!/usr/bin/bash
source ripenv

for i in `ls *.png`; do
    $bin/python3.11 -m getnative --mode all $i
    mv results results-${i%.png}
done
