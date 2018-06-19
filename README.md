# data_process
 对h-strace的跟踪日志文件进行处理，形成进程创建关系图和网络通信关系图
## 各个脚本文件的功能
### gengraph2.sh
总的处理脚本，其会调用各个其他脚本对第1章中的跟踪结果进行处理，形成进程创建关系图和网络通信关系图。

### append_newline.py
由于随时可以ctrl+c关闭strace结束跟踪，因此跟踪生成的tst.log.tid和aaa日志文件结尾可能不是'\n'字符，此脚本就是检查上面的情况，
根据需要在日志文件末尾补充'\n'字符。



### get_thread_list.py
使用方法如下：  
../get_thread_list.py >./get_thread_list.txt  
其会扫描所有的tst.log.tid日志文件，为每个线程生成一条记录并保存到get_thread_list.txt文件，记录格式如下：  
线程tid,所属进程pid,线程名列表  
thread_id:1998 process_id:1998 thread_name_list:"xrdp-sesman","startwm.sh","ssh-agent","dbus-launch","im-launch","x-session-manag","gnome-session-b"



### reg_normalize2.py
对跟踪结果做规范化处理，将不同的字段，通过;;; 符号进行分割。处理结果如下面的示例文件所示：  
https://github.com/ELWIN-MAO/data_process/blob/master/xrdp4/all.core.sort.normal2.txt


type: 1  ;;; serialno: 154  ;;; thread_id: 1938  ;;; process_id: 1453  ;;; thread_name: "xrdp"  ;;; syscall_name: "bind"  ;;; syscall_param: "9<UNIX:[36605]>, {sa_family=AF_LOCAL, sun_path="/tmp/.xrdp/xrdp-9CZDUD/xrdp_000005ad_wm_login_mode_event_00000004_375cd735"}, 110"  ;;; syscall_ret_val: 0  ;;; syscall_ret_val_info: "None"  ;;; errno: "None"  ;;; error_info: "None"  ;;; signal_name: "None"  ;;; signal_param: "None"  ;;; plus_exit_info: "None"

type字段表示，此条记录的类型  
serialno字段表示，此记录发生时的序列号  
thread_id字段表示，此条记录对应的线程tid  
process_id字段表示，此条记录对应的进程pid  
thread_name字段表示，此条记录对应的线程名字  
syscall_name字段表示，此系统调用的名字  
syscall_param字段表示，此系统调用的参数  
syscall_ret_val字段表示，此系统调用的返回值  
syscall_ret_val_info字段表示，返回值对应的信息（例如：返回值为文件描述符时，会被strace解析为文件名  
errno字段表示，系统调用出错时的出错码  
error_info字段表示，系统调用出错码对应的出错含义  
signal_name字段表示，此线程收到了一个信号，并给出了信号名  
plus_exit_info字段表示，线程的退出相关信息（通过执行exit，exit_group系统调用退出或者由于接收到了信号导致退出）  

type字段有5个值含义如下：  
syscall=1 此记录表示一条系统调用事件  
puls_exit_info=2 此记录表示一个进程退出报告事件（通过执行exit，exit_group系统调用退出或者由于接收到了信号导致退出）  
signal=3 此记录表示此线程接收到了一个信号  
detach_syscall=4 此记录表示某个线程脱离了strace跟踪，也就是后续不再对它进程跟踪  
error_pattern=5  表示此记录一个错误的记录，即他不属于上面4个类型的任何一个类型  


### thread_graph.py
使用方法如下：
../thread_graph.py <./all.core.sort.normal2.txt >./all.core.sort.normal2.dot
通过分析clone,execve,send,receive,exit_group等系统调用信息和进程退出的原因。得出进程创建关系图的dot表示，并将错误退出的进程以红色和黄色标记出来。


### thread_graph.py
使用方法如下：  
../commu_graph2.py  > commu_graph2.dot  
通过分析aaa日志文件，形成网络通信关系图的dot表示。



## 代码使用方法：

将h-strace跟踪生成的日志所在的目录（例如test_data目录)拷贝到data_process目录下面。
```
$ cd data_process
$ cp ../gengraph2.sh  .
$ ./gengraph2.sh
```
最终会生成:  
进程创建关系图文件 all.core.sort.normal2.jpg  
进程通信关系图文件 commu_graph2.jpg  



## 分析实例（lxde_logout2，vncserver_3，xrdp4目录中）各个文件的说明

### get_thread_list.txt  
存放各个线程的tid,pid,线程名列表信息。

### all.txt 
 所有的tst.log.tid文件合并后的结果
 
### all.sort.txt
 对all.txt按照序列号排序后的结果
 
### all.core.txt
 对all.txt抽取clone,execve,exit, exit_group和网络通信相关系统调用系统后的结果
 
### all.core.sort.txt
对all.core.txt按照序列号排序后的结果

### aaa.uniq
对aaa日志文件去掉inod缓存失效记录，并进行排序和去重后的结果。主要用来画进程网络通信关系图。


### all.core.sort.normal2.txt
对all.core.sort.txt进行处理，进行类型标记和以";;;"作为字段分隔符后的结果。

### all.core.sort.normal2.dot、all.core.sort.normal2.jpg、all.core.sort.normal2.svg
进程创建关系图的dot,jpg,svg形式表示。

### commu_graph2.dot、commu_graph2.jpg、commu_graph2.svg
网络通信关系图的dot,jpg,svg形式表示。
