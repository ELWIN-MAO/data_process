#!/usr/bin/python3

import sys
import os

import re

#type: enum(syscall=1,exit_with=2,signal=3,detach_syscall=4)
class Syscall_Record:
    def __init__(self):
        self.type=None  
        self.serialno=None
        self.thread_id=None
        self.thread_name=None
        self.syscall_name=None
        self.syscall_param=None
        self.syscall_ret_val=None
        self.syscall_ret_val_info=None
        self.errno=None
        self.error_info=None
        self.signal_name=None
        self.signal_param=None
        self.exit_with_code=None
    def print_str(self):
        print("type:",translate_quote(self.type)," ;;; "+"serialno:",translate_quote(self.serialno)," ;;; "+"thread_id:",translate_quote(self.thread_id)," ;;; "+"thread_name:",translate_quote(self.thread_name)," ;;; "+"syscall_name:",translate_quote(self.syscall_name)," ;;; "+"syscall_param:",translate_quote(self.syscall_param)," ;;; "+"syscall_ret_val:",translate_quote(self.syscall_ret_val)," ;;; "+"syscall_ret_val_info:",translate_quote(self.syscall_ret_val_info)," ;;; "+"errno:",translate_quote(self.errno)," ;;; "+"error_info:",translate_quote(self.error_info)," ;;; "+"signal_name:",translate_quote(self.signal_name)," ;;; "+"signal_param:",translate_quote(self.signal_param)," ;;; "+"exit_with_code:",translate_quote(self.exit_with_code))


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
        aSyscall_Record.serialno=translate(result1.group(1)).strip()
        aSyscall_Record.thread_id=translate(result1.group(3)).strip()
        aSyscall_Record.thread_name="\""+translate(result1.group(5)).strip()+"\""
        aSyscall_Record.syscall_name="\""+translate(result1.group(8)).strip()+"\""
        aSyscall_Record.syscall_param="\""+translate(result1.group(10)).strip()+"\""
        aSyscall_Record.syscall_ret_val=translate(result1.group(14)).strip()
        aSyscall_Record.syscall_ret_val_info="\""+translate(result1.group(20)).strip()+"\""
        aSyscall_Record.errno="\""+translate(result1.group(23)).strip()+"\""
        aSyscall_Record.error_info="\""+translate(result1.group(26)).strip()+"\""       
    elif result2: 
        print("exit_with_syscall")
        print(result2.group(1),result2.group(3),result2.group(5),result2.group(10))
        print("line:",line)
        aSyscall_Record.type=2  
        aSyscall_Record.serialno=translate(result2.group(1)).strip()
        aSyscall_Record.thread_id=translate(result2.group(3)).strip()
        aSyscall_Record.thread_name="\""+translate(result2.group(5)).strip()+"\""
        aSyscall_Record.exit_with_code=translate(result2.group(10)).strip()        
    elif result3: 
        print("signal_syscall")
        print(result3.group(1),result3.group(3),result3.group(5),result3.group(10),result3.group(14))
        print("line:",line)
        aSyscall_Record.type=3  
        aSyscall_Record.serialno=translate(result3.group(1)).strip()
        aSyscall_Record.thread_id=translate(result3.group(3)).strip()
        aSyscall_Record.thread_name="\""+translate(result3.group(5)).strip()+"\""
        aSyscall_Record.signal_name="\""+translate(result3.group(10)).strip()+"\""
        aSyscall_Record.signal_param="\""+translate(result3.group(14)).strip()+"\""      
    elif result4: 
        print("detach_syscall")
        print(result4.group(1),result4.group(3),result4.group(5),result4.group(8))
        print("line:",line)
        aSyscall_Record.type=4  
        aSyscall_Record.serialno=translate(result4.group(1)).strip()
        aSyscall_Record.thread_id=translate(result4.group(3)).strip()
        aSyscall_Record.thread_name="\""+translate(result4.group(5)).strip()+"\""
        aSyscall_Record.syscall_name="\""+translate(result4.group(8)).strip()+"\""       
    else: 
        print("error pattern")
        print(line)
    aSyscall_Record.print_str()
