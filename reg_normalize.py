#!/usr/bin/python3

import sys
import os

import re

#type: enum(syscall=1,exit_with=2,signal=3,detach_syscall=4)
class Syscall_Record:
    def __init__(self):
        self.type=""  
        self.serialno=""
        self.thread_id=""
        self.thread_name=""
        self.syscall_name=""
        self.syscall_param=""
        self.syscall_ret_val=""
        self.syscall_ret_val_info=""
        self.errno=""
        self.error_info=""
        self.signal_name=""
        self.signal_param=""
        self.exit_with_code=""
    def print_str(self):
        print("type:",self.type," ;;; " ,"serialno:",self.serialno," ;;; " ,"thread_id:",self.thread_id," ;;; " ,"thread_name:",self.thread_name," ;;; " ,"syscall_name:",self.syscall_name," ;;; " ,"syscall_param:",self.syscall_param," ;;; " ,"syscall_ret_val:",self.syscall_ret_val," ;;; " ,"syscall_ret_val_info:",self.syscall_ret_val_info," ;;; " ,"errno:",self.errno," ;;; " ,"error_info:",self.error_info," ;;; " ,"signal_name:",self.signal_name," ;;; " ,"signal_param:",self.signal_param," ;;; " ,"exit_with_code:",self.exit_with_code)
    
        
normal_syscall_ptn=r'(\d+)(\s*,\s*)(\d+)(\s+)(([^,\s]+\s*)+)(\s*,\s*)([^\(]+)(\()((.)*)(\))(\s*=\s*)((-?(\d)+)|(\?))(\s+)?(\(([^\(\)]+)\))?(\s+)?((\S+)(\s+)(\()(.+)(\)))?'
normal_syscall_ptn_cmpiled=re.compile(normal_syscall_ptn)


exit_with_ptn=r'(\d+)(\s*,\s*)(\d+)(\s+)(([^,\s]+\s*)+)(\s*,\s*)(\+\+\+ exited with)(\s+)(\S+)(\s+)(\+\+\+)'
exit_with_ptn_cpmiled=re.compile(exit_with_ptn)



signal_syscall_ptn=r'(\d+)(\s*,\s*)(\d+)(\s+)(([^,\s]+\s*)+)(\s*,\s*)(\-\-\-)(\s+)(\S+)(\s+)((\{)([^\{\}]+)(\}))(\s+)(\-\-\-)'
signal_syscall_ptn_cmpiled=re.compile(signal_syscall_ptn)

detach_syscall_ptn=r'(\d+)(\s*,\s*)(\d+)(\s+)(([^,\s]+\s*)+)(\s*,\s*)([^\(]+)(\()(.*)\<detached \.\.\.\>'
detach_syscall_ptn_cmpiled=re.compile(detach_syscall_ptn)

syscall_record={}

log=sys.stdin


while True:
    line=log.readline()
    if not line : break
    result1=normal_syscall_ptn_cmpiled.match(line)
    result2=exit_with_ptn_cpmiled.match(line)
    result3=signal_syscall_ptn_cmpiled.match(line)
    result4=detach_syscall_ptn_cmpiled.match(line)
    aSyscall_Record=Syscall_Record()
    if result1 :
        print("normal_syscall")
        print(result1.group(1),result1.group(3),result1.group(5),result1.group(8),result1.group(10),result1.group(14),result1.group(20),result1.group(23),result1.group(26))
        print("line:",line)
        aSyscall_Record.type=1  
        aSyscall_Record.serialno=result1.group(1).strip()
        aSyscall_Record.thread_id=result1.group(3).strip()
        aSyscall_Record.thread_name="\""+result1.group(5).strip()+"\""
        aSyscall_Record.syscall_name="\""+result1.group(8).strip()+"\""
        aSyscall_Record.syscall_param="\""+result1.group(10).strip()+"\""
        aSyscall_Record.syscall_ret_val=result1.group(14).strip()
        aSyscall_Record.syscall_ret_val_info="\""+result1.group(20).strip()+"\""
        aSyscall_Record.errno="\""+result1.group(23).strip()+"\""
        aSyscall_Record.error_info="\""+result1.group(26).strip()+"\""       
    elif result2: 
        print("exit_with_syscall")
        print(result2.group(1),result2.group(3),result2.group(5),result2.group(10))
        print("line:",line)
        aSyscall_Record.type=2  
        aSyscall_Record.serialno=result2.group(1).strip()
        aSyscall_Record.thread_id=result2.group(3).strip()
        aSyscall_Record.thread_name="\""+result2.group(5).strip()+"\""
        aSyscall_Record.exit_with_code=result2.group(10).strip()        
    elif result3: 
        print("signal_syscall")
        print(result3.group(1),result3.group(3),result3.group(5),result3.group(10),result3.group(14))
        print("line:",line)
        aSyscall_Record.type=3  
        aSyscall_Record.serialno=result3.group(1).strip()
        aSyscall_Record.thread_id=result3.group(3).strip()
        aSyscall_Record.thread_name="\""+result3.group(5).strip()+"\""
        aSyscall_Record.signal_name="\""+result3.group(10).strip()+"\""
        aSyscall_Record.signal_param="\""+result3.group(14).strip()+"\""      
    elif result4: 
        print("detach_syscall")
        print(result4.group(1),result4.group(3),result4.group(5),result4.group(8))
        print("line:",line)
        aSyscall_Record.type=4  
        aSyscall_Record.serialno=result4.group(1).strip()
        aSyscall_Record.thread_id=result4.group(3).strip()
        aSyscall_Record.thread_name="\""+result4.group(5).strip()+"\""
        aSyscall_Record.syscall_name="\""+result4.group(8).strip()+"\""       
    else: 
        print("error pattern")
        print(line)
    aSyscall_Record.print_str()
