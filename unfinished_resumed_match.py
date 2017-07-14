#!/usr/bin/python

import sys
import os

import re


resumed_regex = re.compile(r'<\.\.\. (\S+) resumed>')
unfinished_regex = re.compile(r'<unfinished \.\.\.>$')

log=sys.stdin

class Item:
    def __init__(self):
        self.pid=None
        self.type=None
        self.pname=""
        self.syscallname=""
        self.syscallinfo=""

def fixit(bitem, atplist):
    for i in  range(0,len(atplist))[::-1]:
        if( (atplist[i].type==3) and (0==cmp(atplist[i].pid.strip(), bitem.pid.strip()) ) and(0==cmp(atplist[i].pname.strip(), bitem.pname.strip()) )):
            atplist[i].syscallinfo+=bitem.syscallinfo
            break



resumed_list=[]
normal_unfiniished_list=[]


while True:
    line=log.readline()
    if not line : break
    match=resumed_regex.search(line)   
    if match :
    	print match.group(0)
    	print match.group(1)
        
        aitem=Item()
        words=line.split()
        aitem.type=2
        aitem.pid=words[0]

        for i in range(1,len(words)):
            if (cmp(words[i],",")!=0):
     	    	aitem.pname+=(" "+words[i])
            else :
	    	aitem.syscallname=words[i+2]
	    	for j in range(i+4,len(words)):
	    		aitem.syscallinfo+=(" "+words[j])
                break
        resumed_list.append(aitem)
        print aitem.pid 
        print aitem.pname
        print aitem.syscallname
        print aitem.syscallinfo
        


    match=unfinished_regex.search(line)
    if match :
        print match.group(0)
        #print match.group(1)
        
        aitem=Item()
        words=line.split()
        aitem.type=3
        aitem.pid=words[0]

        for i in range(1,len(words)):
            if (cmp(words[i],",")!=0):
               aitem.pname+=(" "+words[i])
            else :
               tmp=words[i+1]
               tmp2=tmp.split("(")
               aitem.syscallname=tmp2[0]
               aitem.syscallinfo+=tmp2[1]
               for j in range(i+2,len(words)):
                   if (cmp(words[j],"<unfinished")!=0):
                       aitem.syscallinfo+=(" "+words[j])
                   else: 
                        break
               break
        normal_unfiniished_list.append(aitem)
        print aitem.pid 
        print aitem.pname
        print aitem.syscallname
        print aitem.syscallinfo
    else :
        aitem=Item()
        aitem.type=1
        aitem.syscallinfo+=line
        normal_unfiniished_list.append(aitem)

for i in  range(0,len(resumed_list)):
    if(resumed_list[i].type==1):
        print resumed_list[i].syscallinfo
    elif (resumed_list[i].type==3)
        for j in range(
#    print resumed_list[i].pid + " -> " +tplist[i].pname + ","+tplist[i].syscallname+","+tplist[i].syscallinfo
