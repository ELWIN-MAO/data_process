#!/bin/bash -x
cat *.log.* > all.txt

sort -n all.txt  > all.sort.txt

../reg_normalize2.py < ./all.sort.txt  > ./all.sort.normal.txt

../thread_graph.py  <  ./all.sort.normal.txt >./all.sort.normal.dot

dot -Tjpg ./all.sort.normal.dot  -o ./all.sort.normal.jpg
