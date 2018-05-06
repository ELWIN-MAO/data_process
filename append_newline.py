#!/usr/bin/python3
import os
import sys
#os.chdir('./aaa')
movie_name = os.listdir('.')
for temp in movie_name:
    if temp.startswith("tst.log.") or temp=="aaa":
        fo = open(temp, "rb+")
        fo.seek(-1, 2)
        if(bytes.decode(fo.read(1))!="\n"):
            print(temp)
            fo.write(str.encode("\n"))
        fo.close()
