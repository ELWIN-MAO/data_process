#!/usr/bin/python3

import sys
import os

import re


log=sys.stdin


class Thread_Info_Record:
    def __init__(self):
        self.thread_id=None
        self.process_id=None
        self.thread_name_list=[]
        self.execve_list=[]            
        self.write2_list=[]            
        self.children_list=[]
        self.exit_code=None
        self.plus_exit_info=None
        self.syscall_error_info_list=[]
    def print_str(self):    
        print("thread_id:",self.thread_id)
        print("thread_name_list:")
        for aitem in self.thread_name_list:
            print(aitem)
        print("execve_list:")
        for k,v in self.execve_list:
            print(k,v)
        print("children_list:")
        for aitem in self.children_list:
            print(aitem)
        print("exit_code:",self.exit_code)
        #print("syscall_error_info_list:",self.syscall_error_info_list)
    def print_node(self):
        #print("node_begin")
        out=""
        children_edge=""
        out+=self.thread_id+"   [label=\""
        #print(self.thread_id+"[label=\"")
        out+="thread_id:"+self.thread_id+"\\n"
        #print("thread_id:",self.thread_id)
        #print("thread_name_list:")
        out+="thread_name_list:"
        for aitem in self.thread_name_list:
            #print(aitem)
            out+=aitem.replace("\"","\\\"")+","
        if (out[-1]==",") :
            out=out[:-1]
        #out+="\\n"
        #print("execve_list:")
        #for k,v in self.execve_list:
            #print(k,v)
        #print("children_list:")
        #out+="children_list:"
        #for aitem in self.children_list:
            #print(aitem)
        #    out+=aitem[1]+" ,"
        #    children_edge+=self.thread_id+"->"+aitem[1]+"[lable=\""+aitem[0]+"\"];\\n"
        #out+="\""
        #print("exit_code:",self.exit_code)
        for aitem in self.execve_list:
            out+="\\n"+aitem.replace("\"","\\\"")
        #for aitem in self.write2_list[-5:]:
        #    tmp=aitem.replace("\\","\\\\")
        #    out+="\\n"+tmp.replace("\"","\\\"")
        if(self.exit_code):
            out+="\\nexit_code:"+self.exit_code[0]+":"+self.exit_code[1].replace("\"","\\\"")
        if(self.plus_exit_info):
            out+="\\nplus_exit_info:"+self.plus_exit_info[0]+":"+self.plus_exit_info[1].replace("\"","\\\"")
        out+="\""
        
        if(self.thread_id==self.process_id):
            out+=", style = filled "
            if(self.exit_code and self.exit_code  [1]!="\"0\""):
                out+=", color=\"indianred1\""
            if(self.exit_code and self.exit_code  [1]=="\"0\""):
                out+=", color=\"grey77\""
            if((not self.exit_code) and ( not self.plus_exit_info) ):
                out+=", color=\"green3\""
            if((not self.exit_code) and  self.plus_exit_info):
                out+=", color=\"yellow\""
        else : 
            if(self.exit_code and self.exit_code  [1]!="\"0\""):
                out+=", color=\"indianred1\""
        out+="];"
        #out=out.replace("\"","\\\"")
        print(out)
        #print(children_edge)
        #print("node_end")
        #print("syscall_error_info_list:",self.syscall_error_info_list)

    def print_edge(self):
        children_edge=""
        for aitem in self.children_list:
            #print(aitem)
            children_edge+=self.thread_id+" -> "+aitem[1]+"   [label=\""+aitem[0]+"\"];\n"
        print(children_edge) 

thread_info_list=[]
process_info_list=[]
## process_info_list["pid1"]=[list of pid1's threads]
        

def get_thread_info_record(athread_id):
    athread_info=None       
    for thread_info in thread_info_list:
        #if (strcmp(thread_info.thread_id,athread_id)==0):
        if (thread_info.thread_id==athread_id):
            athread_info=thread_info
            break
    if  not athread_info:
        athread_info=Thread_Info_Record()
        athread_info.thread_id=athread_id
        thread_info_list.append(athread_info)
    return athread_info 
        

def get_thread_info_record_not_new(athread_id):
    athread_info=None       
    for thread_info in thread_info_list:
        #if (strcmp(thread_info.thread_id,athread_id)==0):
        if (thread_info.thread_id==athread_id):
            athread_info=thread_info
            break
    if  not athread_info:
        sys.stderr.write("error:"+athread_id+"not found!\n");   
    return athread_info 

def get_sycall_record(line) :
        words=line.split(";;;") 
        aSyscall_Record={}
        for aword in words:
            guard=aword.index(":")
            akey=aword[0:guard].strip()
            avalue=aword[guard+1:].strip()
            aSyscall_Record[akey]=avalue
        return aSyscall_Record


#linecount=0
pre_data="./get_thread_list.txt"        
if(os.path.exists(pre_data)):
    ptn=r'thread_id:([\d]+) process_id:([\d]+) thread_name_list:(.+)\n'
    ptn_cmpiled=re.compile(ptn)
    fo = open(pre_data, "r")
    while True:
        line=fo.readline()
        if not line : break
        athread_info=Thread_Info_Record()
        result1=ptn_cmpiled.match(line)
        if result1:
            athread_info.thread_id=result1.group(1)
            athread_info.process_id=result1.group(2)
            athread_info.thread_name_list=list(result1.group(3).split(","))
            thread_info_list.append(athread_info)
            if athread_info.process_id not in process_info_list:
                process_info_list.append(athread_info.process_id)
        else:
            sys.stderr.write("threadgraph content error\n")
            sys.stderr.write(line+"\n")
            sys.exit(1)
    fo.close()


while True:
    line=log.readline()
    if not line : break 
    #linecount+=1
    #print(line)
    #print("linecount:"+str(linecount))
    aSyscall_Record=get_sycall_record(line)
    aThread_Info_Record=get_thread_info_record(aSyscall_Record["thread_id"])
    #if aThread_Info_Record is not eixst, will allocate a new record
    if(aSyscall_Record["type"]=="2"):
        if  ( "killed by" in aSyscall_Record["plus_exit_info"]) :
            aThread_Info_Record.plus_exit_info=[aSyscall_Record["serialno"],aSyscall_Record["plus_exit_info"]]
    #every line need to update thread_name
    if(aSyscall_Record["type"]!="2" and aSyscall_Record["type"]!="5"):
    # only type==2 record ,that  maybe contain pid==-1 and comm=NULL
    # here we can get correct process id info 
        aThread_Info_Record.process_id=aSyscall_Record["process_id"]
        ##record aproces contain which tids
        if  not( aSyscall_Record["thread_name"]  in aThread_Info_Record.thread_name_list):
            aThread_Info_Record.thread_name_list.append(aSyscall_Record["thread_name"])
        if not(aSyscall_Record["process_id"] in  process_info_list):
            process_info_list.append(aSyscall_Record["process_id"])
    if(aSyscall_Record["type"]=="1"):
        if(aSyscall_Record["syscall_name"]=="\"clone\"" or aSyscall_Record["syscall_name"]=="\"vfork\""):
            aThread_Info_Record.children_list.append([aSyscall_Record["serialno"],aSyscall_Record["syscall_ret_val"]])
        if( (aSyscall_Record["syscall_name"]=="\"exit\"")  or (aSyscall_Record["syscall_name"]=="\"exit_group\"")):
            aThread_Info_Record.exit_code=[aSyscall_Record["serialno"],aSyscall_Record["syscall_param"]]
        if(aSyscall_Record["syscall_name"]=="\"execve\""):
            aThread_Info_Record.execve_list.append("execve:"+aSyscall_Record["serialno"]+":"+aSyscall_Record["syscall_param"].split(",")[0][1:]+"="+aSyscall_Record["syscall_ret_val"])
        if((aSyscall_Record["syscall_name"]=="\"write\"" or aSyscall_Record["syscall_name"]=="\"writev\"" ) and aSyscall_Record["syscall_param"][1]=="2"):
            aThread_Info_Record.write2_list.append("write2:"+aSyscall_Record["serialno"]+":"+aSyscall_Record["syscall_param"])
        if(aSyscall_Record["errno"]!="\"None\""):
            aThread_Info_Record.syscall_error_info_list.append([aSyscall_Record["errno"],aSyscall_Record["error_info"]])
    #aThread_Info_Record.print_str()


print("digraph abc{")
for item in process_info_list:
    print("subgraph cluster_"+item+" {")
    for thread_info in thread_info_list:
        if (thread_info.process_id==item):
            thread_info.print_node()
    print("label = "+"\"process #"+item+"\";") 
    print("color = blue;")
    print("}")

for item in thread_info_list:
    #item.print_str()
    item.print_edge()

#pre_data="./aaa.uniq"
#if(os.path.exists(pre_data)):
#    ptn8=r'current_tid:([\d]+) socket_type:(\S+) addr:(\S+) socket_to_pid_result:([\d]+)\n'
#    ptn8_cmpiled=re.compile(ptn8)
#    fo = open(pre_data, "r")
#    while True:
#        line=fo.readline()
#        if not line : break
#        result8=ptn8_cmpiled.match(line)
#        if result8:
#            src_tid=result8.group(1)
#            socket_name=result8.group(2)+":"+result8.group(3)
#            dest_pids=result8.group(4)
#            dest_pid_list=dest_pids.split(",")
#            for apid in  dest_pid_list:
#                #print(src_tid+" -> "+apid+" [label=\""+socket_name+"\" , color=\"purple\" ];\n")
#                print(src_tid+" -> "+apid+";\n")
#        else:
#            sys.stderr.write("aaa.uniq  content error\n")
#            sys.stderr.write(line)

print("}")


#for thread_info int thread_info_list:
#   print each GRAPH NODE NAME
    
# for thread_info int thread_info_list:
    # print each edeget with serial no  
    
