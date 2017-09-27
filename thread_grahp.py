#!/usr/bin/python3

import sys
import os

import re

##需要解决None变量没有append方法的问题，需要解决字符串比较的时候使用cmp的问题。
##对应返回值不为0的节点要做特殊的标注，使用方块形状的节点表示出来。


log=sys.stdin


class Thread_Info_Record:
    def __init__(self):
        self.thread_id=None
        self.thread_name_list=[]
        self.execve_list=[]            
        self.children_list=[]
        self.exit_code=None
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
        print("syscall_error_info_list:",self.syscall_error_info_list)
        

thread_info_list=[]
        

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
        


def get_sycall_record(line ) :
        words=line.split(";;;") 
        aSyscall_Record={}
        for aword in words:
            k_v=aword.split(":")
            #print(k_v)
            aSyscall_Record[k_v[0].strip()]=k_v[1].strip()
        return aSyscall_Record



        
while True:
    line=log.readline()
    if not line : break 
    print("line:",line)
    aSyscall_Record=get_sycall_record(line)
    aThread_Info_Record=get_thread_info_record(aSyscall_Record["thread_id"])
    #every line need to update thread_name
    if  not( aSyscall_Record["thread_name"]  in aThread_Info_Record.thread_name_list):
        aThread_Info_Record.thread_name_list.append(aSyscall_Record["thread_name"])
    if(aSyscall_Record["type"]=="1"):
        #if(strcmp(aSyscall_Record["syscall_name"],"clone")==0):
        if(aSyscall_Record["syscall_name"]=="\"clone\""):
            aThread_Info_Record.children_list.append([aSyscall_Record["serialno"],aSyscall_Record["syscall_ret_val"]])
        if( (aSyscall_Record["syscall_name"]=="\"exit\"")  or (aSyscall_Record["syscall_name"]=="\"exit_group\"")):
            aThread_Info_Record.exit_code=[aSyscall_Record["serialno"],aSyscall_Record["syscall_param"]]
        if(aSyscall_Record["syscall_name"]=="\"execve\""):
            aThread_Info_Record.execve_list.append([aSyscall_Record["serialno"],aSyscall_Record["syscall_param"]])
        if(aSyscall_Record["errno"]!="\"None\""):
            aThread_Info_Record.syscall_error_info_list.append([aSyscall_Record["errno"],aSyscall_Record["error_info"]])
    aThread_Info_Record.print_str()


for item in thread_info_list:
    item.print_str()


# for thread_info int thread_info_list:
    # print each GRAPH NODE NAME
    
# for thread_info int thread_info_list:
    # print each edeget with serial no  
    