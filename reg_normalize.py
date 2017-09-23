import sys
import os

import re

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
    if result1 :
        print("normal_syscall")
        print(result1.group(1),result1.group(3),result1.group(5),result1.group(8),result1.group(10),result1.group(14),result1.group(20),result1.group(23),result1.group(26))
        print("line:",line)
    elif result2: 
        print("exit_with_syscall")
        print(result2.group(1),result2.group(3),result2.group(5),result2.group(10))
        print("line:",line)
    elif result3: 
        print("signal_syscall")
        print(result3.group(1),result3.group(3),result3.group(5),result3.group(10),result3.group(14))
        print("line:",line)
    elif result4: 
        print("detach_syscall")
        print(result4.group(1),result4.group(3),result4.group(5),result4.group(8))
        print("line:",line)
    else: 
        print("error pattern")
        print(line)
