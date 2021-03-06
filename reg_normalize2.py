#!/usr/bin/python3

import sys
import os

import re

#type: enum(syscall=1,puls_exit_info=2,signal=3,detach_syscall=4,error_pattern=5)
class Syscall_Record:
    def __init__(self):
        self.type=None  
        self.serialno=None
        self.thread_id=None
        self.process_id=None
        self.thread_name=None
        self.syscall_name=None
        self.syscall_param=None
        self.syscall_ret_val=None
        self.syscall_ret_val_info=None
        self.errno=None
        self.error_info=None
        self.signal_name=None
        self.signal_param=None
        self.plus_exit_info=None
    def print_str(self):
        print("type:",translate_quote(self.type)," ;;; "+"serialno:",translate_quote(self.serialno)," ;;; "+"thread_id:",translate_quote(self.thread_id)," ;;; "+"process_id:",translate_quote(self.process_id)," ;;; "+"thread_name:",translate_quote(self.thread_name)," ;;; "+"syscall_name:",translate_quote(self.syscall_name)," ;;; "+"syscall_param:",translate_quote(self.syscall_param)," ;;; "+"syscall_ret_val:",translate_quote(self.syscall_ret_val)," ;;; "+"syscall_ret_val_info:",translate_quote(self.syscall_ret_val_info)," ;;; "+"errno:",translate_quote(self.errno)," ;;; "+"error_info:",translate_quote(self.error_info)," ;;; "+"signal_name:",translate_quote(self.signal_name)," ;;; "+"signal_param:",translate_quote(self.signal_param)," ;;; "+"plus_exit_info:",translate_quote(self.plus_exit_info))


def translate(a):
    if a:
        return a
    else:
        return "None"   

def translate_quote(a):
    if a:
        return a
    else:
        return "\"None\""         
        
normal_syscall_ptn=r'(\d+)(\s*,\s*)(\d+)(\s*,\s*)(-?\d+)(\s*,\s*)(([^,\s]+\s*)+)(\s*,\s*)([^\(]+)(\()((.)*)(\))(\s*=\s*)((-?(\d)+)|(\?))(\s+)?(\(([^\(\)]+)\))?(\s+)?((\S+)(\s+)(\()(.+)(\)))?'
normal_syscall_ptn_cmpiled=re.compile(normal_syscall_ptn)


#exit_with_ptn=r'(\d+)(\s*,\s*)(\d+)(\s+)(([^,\s]+\s*)+)(\s*,\s*)(\+\+\+ exited with)(\s+)(\S+)(\s+)(\+\+\+)'
#exit_with_ptn_cpmiled=re.compile(exit_with_ptn)

plus_exit_info_ptn=r'(\d+)(\s*,\s*)(\d+)(\s*,\s*)(-?\d+)(\s*,\s*)(([^,\s]+\s*)+)(\s*,\s*)(\+\+\+)([^\(\)]+)(\+\+\+)'
plus_exit_info_ptn_cmpiled=re.compile(plus_exit_info_ptn)


signal_syscall_ptn=r'(\d+)(\s*,\s*)(\d+)(\s*,\s*)(-?\d+)(\s*,\s*)(([^,\s]+\s*)+)(\s*,\s*)(\-\-\-)(\s+)(\S+)(\s+)((\{)([^\{\}]+)(\}))(\s+)(\-\-\-)'
signal_syscall_ptn_cmpiled=re.compile(signal_syscall_ptn)

detach_syscall_ptn=r'(\d+)(\s*,\s*)(\d+)(\s*,\s*)(-?\d+)(\s*,\s*)(([^,\s]+\s*)+)(\s*,\s*)([^\(]+)(\()(.*)\<(detached|unfinished) \.\.\.\>'
detach_syscall_ptn_cmpiled=re.compile(detach_syscall_ptn)

#plus_info_ptn=r'(\d+)(\s*,\s*)(\d+)(\s+)(([^,\s]+\s*)+)(\s*,\s*)(\+\+\+)([^\(\)]+)(\+\+\+)'
#plus_info_ptn_cmpiled=re.compile(plus_info_ptn)



syscall_record={}

log=sys.stdin


while True:
    line=log.readline()
    if not line : break
    line=line.replace(";;;","\\;\\;\\;")
    result1=normal_syscall_ptn_cmpiled.match(line)
    result2=plus_exit_info_ptn_cmpiled.match(line)
    result3=signal_syscall_ptn_cmpiled.match(line)
    result4=detach_syscall_ptn_cmpiled.match(line)
    aSyscall_Record=Syscall_Record()
    flag=0
    if result1 :
#        print("normal_syscall")
#        print(result1.group(1),result1.group(3),result1.group(5),result1.group(8),result1.group(10),result1.group(14),result1.group(20),result1.group(23),result1.group(26))
#        print("line:",line)
        aSyscall_Record.type=1  
        aSyscall_Record.serialno=translate(result1.group(1)).strip()
        aSyscall_Record.thread_id=translate(result1.group(3)).strip()
        aSyscall_Record.process_id=translate(result1.group(5)).strip()
        aSyscall_Record.thread_name="\""+translate(result1.group(7)).strip()+"\""
        aSyscall_Record.syscall_name="\""+translate(result1.group(10)).strip()+"\""
        aSyscall_Record.syscall_param="\""+translate(result1.group(12)).strip()+"\""
        aSyscall_Record.syscall_ret_val=translate(result1.group(16)).strip()
        aSyscall_Record.syscall_ret_val_info="\""+translate(result1.group(22)).strip()+"\""
        aSyscall_Record.errno="\""+translate(result1.group(25)).strip()+"\""
        aSyscall_Record.error_info="\""+translate(result1.group(28)).strip()+"\""       
    elif result2: 
        # for exam
        #52 , 13965 , -1 , NULL , +++ exited with 0 +++
        #41359 , 22939 , -1 , NULL , +++ killed by SIGTERM +++
        #maybe we need write this info into another log file,other than the stdout
#        print("exit_with_syscall")
#        print(result2.group(1),result2.group(3),result2.group(5),result2.group(10))
#        print("line:",line)
        aSyscall_Record.type=2  
        aSyscall_Record.serialno=translate(result2.group(1)).strip()
        aSyscall_Record.thread_id=translate(result2.group(3)).strip()
        aSyscall_Record.process_id=translate(result2.group(5)).strip()
        aSyscall_Record.thread_name="\""+translate(result2.group(7)).strip()+"\""
        aSyscall_Record.plus_exit_info="\""+translate(result2.group(11)).strip()+"\""        
    elif result3: 
#        print("signal_syscall")
#        print(result3.group(1),result3.group(3),result3.group(5),result3.group(10),result3.group(14))
#        print("line:",line)
        aSyscall_Record.type=3  
        aSyscall_Record.serialno=translate(result3.group(1)).strip()
        aSyscall_Record.thread_id=translate(result3.group(3)).strip()
        aSyscall_Record.process_id=translate(result3.group(5)).strip()
        aSyscall_Record.thread_name="\""+translate(result3.group(7)).strip()+"\""
        aSyscall_Record.signal_name="\""+translate(result3.group(12)).strip()+"\""
        aSyscall_Record.signal_param="\""+translate(result3.group(16)).strip()+"\""      
    elif result4: 
 #       print("detach_syscall")
 #       print(result4.group(1),result4.group(3),result4.group(5),result4.group(8))
 #       print("line:",line)
        aSyscall_Record.type=4  
        aSyscall_Record.serialno=translate(result4.group(1)).strip()
        aSyscall_Record.thread_id=translate(result4.group(3)).strip()
        aSyscall_Record.process_id=translate(result4.group(5)).strip()
        aSyscall_Record.thread_name="\""+translate(result4.group(7)).strip()+"\""
        aSyscall_Record.syscall_name="\""+translate(result4.group(10)).strip()+"\""       
    else: 
        #type=5 means error pattern
        aSyscall_Record.type=5
        #print("error_pattern",end="")
        #print(line)
    aSyscall_Record.print_str()
