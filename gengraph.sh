#!/bin/bash -x
cat *.log.* > all.txt

sort -n all.txt  > all.sort.txt

../reg_normalize2.py < ./all.sort.txt  > ./all.sort.normal2.txt

#../thread_graph.py  <  ./all.sort.normal.txt >./all.sort.normal.dot
../thread_graph.py  <  ./all.sort.normal2.txt >./all.sort.normal2.dot

#dot -Tjpg ./all.sort.normal.dot  -o ./all.sort.normal.jpg
dot -Tjpg ./all.sort.normal2.dot  -o ./all.sort.normal2.jpg
dot -Tsvg ./all.sort.normal2.dot  -o ./all.sort.normal2.svg
