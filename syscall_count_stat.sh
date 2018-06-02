#!/bin/bash


grep -w  -E "\<UNIX:"    ./all.sort.txt  |  grep -E ", read\(|, write\(|, writev\(|, recvfrom\(|, sendto\(|, recvmsg\(|, sendmsg\(|, send\(|, recv\(|, sendmmsg\(|, recvmmsg\(" |wc -l




grep -w  -E "\<TCP:|\<TCPv6:"    ./all.sort.txt  |  grep -E ", read\(|, write\(|, writev\(|, recvfrom\(|, sendto\(|, recvmsg\(|, sendmsg\(|, send\(|, recv\(|, sendmmsg\(|, recvmmsg\(" |wc -l


total=`grep -w  -E "\<UNIX:|\<TCP:|\<TCPv6:"    ./all.sort.txt  |  grep -E ", read\(|, write\(|, writev\(|, recvfrom\(|, sendto\(|, recvmsg\(|, sendmsg\(|, send\(|, recv\(|, sendmmsg\(|, recvmmsg\(" |wc -l`

echo $total

grep insert ./aaa | wc -l

socket_to_pid_count=`grep socket_to_pid_result ./aaa | wc -l`

echo $socket_to_pid_count

acclerate_rate=`echo "scale=2;$total/$socket_to_pid_count"|bc`
echo $acclerate_rate
