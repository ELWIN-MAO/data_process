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


##Item.type==1  this line is a normal syscall 
##Item.type==2  this line is a resumed syscall
##Item.type==3  this line is a unfinished syscall



def fixit(bitem, atplist):
    for i in  range(0,len(atplist)):
        if( (atplist[i].type==3) and (0==cmp(atplist[i].pid.strip(), bitem.pid.strip()) ) and(0==cmp(atplist[i].pname.strip(), bitem.pname.strip()) )):
            atplist[i].syscallinfo+=bitem.syscallinfo
            atplist[i].type=1
            break



resumed_list=[]
##resumed (type==2) syscall is in this list

normal_unfinished_list=[]
##normal(type==1)and unfinished syscall in this list


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
        normal_unfinished_list.append(aitem)
        print aitem.pid 
        print aitem.pname
        print aitem.syscallname
        print aitem.syscallinfo
    else :
        aitem=Item()
        aitem.type=1
        aitem.syscallinfo+=line
        ## normal syscall info record the whole line, and then print it again
        normal_unfinished_list.append(aitem)
print "begin fixsyscall"


for i in  range(0,len(resumed_list)):
    if(resumed_list[i].type==2):
        print resumed_list[i].syscallinfo
        fixit(resumed_list[i],normal_unfinished_list)

print "begin print all fixed data"

for i in range(0,len(normal_unfinished_list)):
    if(normal_unfinished_list[i].type !=1):
        print normal_unfinished_list[i].pid + " -> " +normal_unfinished_list[i].pname + ","+normal_unfinished_list[i].syscallname+","+normal_unfinished_list[i].syscallinfo
    else :
        print normal_unfinished_list[i].syscallinfo
        #for the normal syscall info(type==1) just print it's original line content
#    print resumed_list[i].pid + " -> " +tplist[i].pname + ","+tplist[i].syscallname+","+tplist[i].syscallinfo
