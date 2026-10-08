[English](position-parse.md) | 简体中文

**GPS模块解析位置信息**

**1. 学习目标**

本次课程我们主要学习使用Jetson Orin和GPS模块实读取并解析位置信息。

**2. 课前准备**

GPS模块采用的是UART通讯或USB通讯，这里以USB通讯为例。

![img](1.png)

使用type-c线连接Jetson Orin和GPS模块，运行命令 ls /dev | grep 'ttyUSB' ，可以看到识别到GPS模块为USB0

![img](2.jpg) 

**3****. 程序**

本次课程的程序请参考：GPS.py

初始化USB：

![img](3.jpg) 

位置信息获取和解析函数，下图中在位置信息中筛选出GNGGA开头的位置信息，然后解析出数据存到各个全局变量中。

![img](4.jpg) 

![img](5.jpg) 

同样的方法获取了GNVTG的航向信息并解析。

![img](6.jpg) 

解析后的数据循环打印

![img](7.jpg) 

**4. 运行程序**

终端输入sudo python3 GPS.py运行程序。

**5.实验现象**

模块通电后，需要32s左右的时间启动，之后模块上的串口打印状态灯会持续闪烁，此时可以正常接收数据。

程序运行以后，开始初始化USB，初始化成功显示“GPS Serial Opened! Baudrate=9600”，否则显示“GPS Serial Open Failed!”，如果错误需要检查接线或USB端口，之后循环打印位置和航向信息。

![img](8.jpg) 

按Ctrl+C退出信息读取。

![img](9.jpg) 

注意，模块天线需要在室外，否则可能搜索不到GPS信号，搜索不到信号的时候打印"GPS no found"。