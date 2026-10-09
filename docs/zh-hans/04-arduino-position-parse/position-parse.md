[English](../../en/04-arduino-position-parse/position-parse.md) | [Deutsch](../../de/04-arduino-position-parse/position-parse.md) | [Español](../../es/04-arduino-position-parse/position-parse.md) | [Français](../../fr/04-arduino-position-parse/position-parse.md) | [Italiano](../../it/04-arduino-position-parse/position-parse.md) | [日本語](../../ja/04-arduino-position-parse/position-parse.md) | [한국어](../../ko/04-arduino-position-parse/position-parse.md) | [Português (BR)](../../pt-br/04-arduino-position-parse/position-parse.md) | [Português (PT)](../../pt-pt/04-arduino-position-parse/position-parse.md) | 简体中文 | [繁體中文](../../zh-hant/04-arduino-position-parse/position-parse.md)

**GPS位置信息解析**

**1. 学习目标**

本次课程我们主要学习使用arduino和GPS模块实现位置信息解析并打印功能。

**2. 课前准备**

GPS模块采用的是UART和USB通讯，这里使用arduino UNO的UART口读取信息，将模块的TX连接arduino UNO板子的D0引脚。VCC和GND分别连接5V和GND。

![img](../../en/04-arduino-position-parse/images/1.png)

**3.** **程序**

初始化串口。

![img](../../en/04-arduino-position-parse/images/2.jpg) 

读取串口数据。

![img](../../en/04-arduino-position-parse/images/3.jpg) 

解析串口数据。

![img](../../en/04-arduino-position-parse/images/4.jpg) 

打印解析之后的位置信息。

![img](../../en/04-arduino-position-parse/images/5.jpg) 

**4. 编译下载程序**

4.1 我们需要通用Arduino IDE软件打开文件，然后点击菜单栏中的“√”编译程序，并且等待左下角出现“编译成功”的字样。

 ![img](../../en/04-arduino-position-parse/images/6.jpg)

4.2 在Arduino IDE的菜单栏中，我们需要选择【工具】---【端口】---选择设备管理器中刚刚显示端口号，如下图所示。

![img](../../en/04-arduino-position-parse/images/7.jpg) 

4.3 选择完成后，点击菜单栏下的“→”将代码上传到UNO板。 当左下角出现“上传完成”字样时，表示程序已成功上传到UNO板，如下图所示。

![img](../../en/04-arduino-position-parse/images/8.jpg) 

 

**5. 实验现象**

模块通电后，需要32s左右的时间启动，之后模块上的串口打印状态灯会持续闪烁，此时可以正常接收数据。

程序下载后运行，打开串口监视窗口，打开串口软件，波特率设置为9600，串口会循环打印解析过的实时位置信息。

![img](../../en/04-arduino-position-parse/images/9.jpg) 

注意，模块天线需要在室外，否则可能搜索不到GPS信号。