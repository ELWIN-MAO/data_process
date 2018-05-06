#!/bin/bash

for adir in `ls`;
do 
echo $adir;
if [ -d $adir ]; 
then
echo "222"; 
echo $adir; 
cd $adir
ls -lh  ./gengraph.sh 
./gengraph.sh
cd -
fi; 
done
