[English](../../en/02-51-microcontroller/gps-data-parsing.md) | [Deutsch](../../de/02-51-microcontroller/gps-data-parsing.md) | [Español](../../es/02-51-microcontroller/gps-data-parsing.md) | [Français](../../fr/02-51-microcontroller/gps-data-parsing.md) | [Italiano](../../it/02-51-microcontroller/gps-data-parsing.md) | [日本語](../../ja/02-51-microcontroller/gps-data-parsing.md) | [한국어](../../ko/02-51-microcontroller/gps-data-parsing.md) | [Português (BR)](../../pt-br/02-51-microcontroller/gps-data-parsing.md) | [Português (PT)](../../pt-pt/02-51-microcontroller/gps-data-parsing.md) | 简体中文 | [繁體中文](../../zh-hant/02-51-microcontroller/gps-data-parsing.md)

**GPS数据解析**

**1. 学习目标**

本次课程我们主要学习使用STC89C52RC型号的51单片机和GPS模块实现位置信息解析功能。

**2. 课前准备**

GPS模块采用的是UART和USB通讯，这里使用C51的UART口读取信息，将模块的TX连接51板子的P3.0引脚。VCC和GND分别连接5V和GND。

![img](../../en/02-51-microcontroller/images/1.png)

**3.** **程序**

初始化串口和数据数组

![img](../../en/02-51-microcontroller/images/2.jpg) 

读取并解析接收到的数据。

![img](../../en/02-51-microcontroller/images/3.jpg) 

通过串口打印接收到的数据。

![img](../../en/02-51-microcontroller/images/4.jpg) 

**4****. 实验现象**

模块通电后，需要32s左右的时间启动，之后模块上的串口打印状态灯会持续闪烁，此时可以正常接收数据。

程序下载后运行，打开串口软件，波特率设置为9600，串口会循环打印现在的位置信息。

![img](../../en/02-51-microcontroller/images/5.jpg) 

注意，模块天线需要在室外，否则可能搜索不到GPS信号。