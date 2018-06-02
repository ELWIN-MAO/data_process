#!/bin/bash

for adirent in `ls`;
do 
echo $adirent;
if [ -d $adirent ]; 
then
echo "222"; 
echo $adirent; 
cd $adirent
cp ../gengraph2.sh .
./gengraph2.sh
cd -
fi; 
done
