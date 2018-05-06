#!/usr/bin/python3
import os
import sys
import re

#os.chdir('./aaa')

class Thread_Info_Record:
    def __init__(self):
        self.thread_id=None
        self.process_id=None
        self.thread_name_list=[]
    def print_str(self):
        sys.stdout.write("thread_id:"+self.thread_id+" ")
        sys.stdout.write("process_id:"+self.process_id+" ")
        new_list=[]
        for at in self.thread_name_list:
            new_list.append("\""+at+"\"")
        sys.stdout.write("thread_name_list:"+",".join(new_list))
        print()
    def __lt__(self, other):
        return int(self.thread_id)<int(other.thread_id)
        


ptn=r'([\d]+ , )([\d]+)( , )((-1)|[\d]+)( , )((NULL)|([^\,]+))( ,.*\n)'
ptn_cmpiled=re.compile(ptn)


thread_info_list=[]
process_info_list=[]


movie_name = os.listdir('.')


for temp in movie_name:
    if temp.startswith("tst.log."):
        #print(temp)
        fo = open(temp, "r")
        fo_tmp=open("_t", "w")
        athread_info=Thread_Info_Record()
        while True:
            line=fo.readline()
            if not line : break
            result1=ptn_cmpiled.match(line)
            if result1:
                if result1.group(4)!="-1":
                    fo_tmp.write(line)
                    athread_info.thread_id=result1.group(2)
                    athread_info.process_id=result1.group(4)
                    #print(result1.group(7))
                    #print(athread_info.thread_name_list)
                    if len(athread_info.thread_name_list)>0:
                        if athread_info.thread_name_list[-1]!=result1.group(7):
                            athread_info.thread_name_list.append(result1.group(7))
                    else:
                        athread_info.thread_name_list.append(result1.group(7))
                    #print("--------------")
                    #print(result1.group(7))
                    #print(athread_info.thread_name_list)
                else:
                    newline=list(result1.group(1,2,3,4,6,7,10))
                    #print(athread_info.process_id)
                    #print(athread_info.thread_id)
                    #print(athread_info.thread_name_list)
                    newline[3]=athread_info.process_id
                    newline[5]=athread_info.thread_name_list[-1]
                    newline_str="".join(newline)
                    #sys.stdout.write(newline_str)
                    fo_tmp.write(newline_str)
            else:
                sys.stderr.write("get_thread_list content error\n")
                sys.stderr.write(temp+"\n")
                sys.stderr.write(line)
                sys.exit(1)
        fo.close()
        fo_tmp.close()
        os.rename("_t",temp)

        thread_info_list.append(athread_info)
        if athread_info.process_id not in process_info_list:
            process_info_list.append(athread_info.process_id)

thread_info_list.sort()
for at in thread_info_list:
    at.print_str()

#for bt in process_info_list:
#    print(bt)
