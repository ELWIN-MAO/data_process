#!/usr/bin/python3
import os
import sys
import re

#linecount=0
tid_tname_dic={}
tid_pid_dic={}
pid_list=[]
pre_data="./get_thread_list.txt"
if(os.path.exists(pre_data)):
    ptn=r'thread_id:([\d]+) process_id:([\d]+) thread_name_list:(.+)\n'
    ptn_cmpiled=re.compile(ptn)
    fo = open(pre_data, "r")
    while True:
        line=fo.readline()
        if not line : break
        result1=ptn_cmpiled.match(line)
        if result1:
            tid_tname_dic[result1.group(1)]=result1.group(3)
            tid_pid_dic[result1.group(1)]=result1.group(2)
            if result1.group(2) not in pid_list:
                pid_list.append(result1.group(2))
        else:
            sys.stderr.write("threadgraph content error\n")
            sys.stderr.write(line+"\n")
            sys.exit(1)
    fo.close()
else :
    sys.stderr.write("./get_thread_list.txt not found\n")
    sys.exit(1)



com_tid_list=[]
edege_str=""
ptn8=r'current_tid:([\d]+) socket_type:(\S+) addr:(\S+) socket_to_pid_result:(([\d]+)(,[\d]+)*)\n'
ptn8_cmpiled=re.compile(ptn8)

fo = open("aaa.uniq", "r")
while True:
    line=fo.readline()
    if not line : break
    result8=ptn8_cmpiled.match(line)
    if result8:
        src_tid=result8.group(1)
        if src_tid not in com_tid_list:
            com_tid_list.append(src_tid)
        socket_name=result8.group(2)+":"+result8.group(3)
        dest_pids=result8.group(4)
        dest_pid_list=dest_pids.split(",")
        for apid in  dest_pid_list:
            if apid not in com_tid_list:
                com_tid_list.append(apid)
            #print(src_tid+" -> "+apid+" [label=\""+socket_name+"\" , color=\"purple\" ];\n")
            edege_str+=src_tid+" -> "+apid+" [ color=\"purple\" ];\n"
    else:
        sys.stderr.write("aaa.uniq  content error\n")
        sys.stderr.write(line)
print("digraph abc{")


for item in pid_list:
    print("subgraph cluster_"+item+" {")
    for apid in com_tid_list:
        if (tid_pid_dic[apid]==item):
             print(apid + " [label=\"" + apid +" "+ tid_tname_dic[apid].replace("\"","\\\"") +"\" ];")
    print("label = "+"\"process #"+item+"\";")
    print("color = blue;")
    print("}")

print(edege_str)
print("}")
