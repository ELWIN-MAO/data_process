#!/usr/bin/python

import sys
import os


log=sys.stdin
#log=open(sys.argv[1],'r')

#mylocal=sys.argv[1]
#mypeer=sys.argv[2]

def fixit(bitem, atplist):
   #for i in  range(0,len(tplist)).reverse():
   #arr=range(0,len(tplist))
   #arr=arr.reverse()
   #for i in  arr:
    for i in  range(0,len(tplist))[::-1]:
        if(atplist[i].ppid==bitem.ppid) :
	    atplist[i].pid=bitem.pid
	    break
        #print "error"+ bitem.pid +"  not found"

class Item:
    def __init__(self):
        self.ppid=None
        self.pid=None
tplist=[]
while True:
    line=log.readline()
    if not line : break
    words=line.split()
    aitem=Item()
    aitem.ppid=words[0]
    if "<unfinished\ ...>" in line :
        aitem.pid=NULL	
    else :
        aitem.pid= words[-1]
    if "<... clone resumed>" in line: 
        fixit(aitem, tplist)
    else : 
        tplist.append(aitem)

#for i in  range(0,len(tplist)).reverse():
for i in  range(0,len(tplist)):
    print tplist[i].ppid + " -> " +tplist[i].pid + "[label=" + "\"" +str(i+1) +"\"" + "];"
		   
	



   
