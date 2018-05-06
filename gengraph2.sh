#!/bin/bash -x
../append_newline.py
../get_thread_list.py >./get_thread_list.txt 
cat *.log.* > all.txt

sort  -n all.txt  > all.sort.txt

grep -E  ", clone\(|, execve\(|, exit\(|, exit_group\(|, write\(2<|, writev\(2<|, vfork\(| \+\+\+ killed by|, bind\(|, connect\(" ./all.txt  > all.core.txt

sort -n all.core.txt > all.core.sort.txt

grep -v invalid ./aaa  | cut -d " "  -f 1-4 | sort | uniq >./aaa.uniq

../reg_normalize2.py <./all.core.sort.txt  >./all.core.sort.normal2.txt

../thread_graph.py <./all.core.sort.normal2.txt >./all.core.sort.normal2.dot

dot -Tjpg ./all.core.sort.normal2.dot -o ./all.core.sort.normal2.jpg


../commu_graph.py  > commu_graph.dot

dot -Tjpg ./commu_graph.dot  -o ./commu_graph.jpg

../commu_graph2.py  > commu_graph2.dot

dot -Tjpg ./commu_graph2.dot  -o ./commu_graph2.jpg



../thread_graph_no_write2.py   <./all.core.sort.normal2.txt >./all.core.sort.normal2_no_write2.dot

dot -Tjpg   ./all.core.sort.normal2_no_write2.dot  -o   ./all.core.sort.normal2_no_write2.jpg
