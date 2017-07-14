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
    for i in  range(0,len(atplist))[::-1]:
        if( (atplist[i].ppid==bitem.ppid) and (atplist[i].pid is None) ) :
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
    if "<unfinished ...>" in line :
        aitem.pid=None
        tplist.append(aitem)
    elif "<... clone resumed>" in line :
        aitem.pid=words[-1]
        fixit(aitem, tplist)
    else : 
        aitem.pid= words[-1]
        tplist.append(aitem)
    #print aitem.ppid +":"+ aitem.pid

#for i in  range(0,len(tplist)).reverse():
print "digraph G {"
for i in  range(0,len(tplist)):
    print tplist[i].ppid + " -> " +tplist[i].pid + "[label=" + "\"" +str(i+1) +"\"" + "];"
print "}" 
	



   
