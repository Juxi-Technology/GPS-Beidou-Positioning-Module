[English](../../en/03-arduino-position-read/position-read.md) | [Deutsch](../../de/03-arduino-position-read/position-read.md) | [Español](../../es/03-arduino-position-read/position-read.md) | [Français](../../fr/03-arduino-position-read/position-read.md) | [Italiano](../../it/03-arduino-position-read/position-read.md) | [日本語](../../ja/03-arduino-position-read/position-read.md) | [한국어](../../ko/03-arduino-position-read/position-read.md) | [Português (BR)](../../pt-br/03-arduino-position-read/position-read.md) | [Português (PT)](../../pt-pt/03-arduino-position-read/position-read.md) | 简体中文 | [繁體中文](../../zh-hant/03-arduino-position-read/position-read.md)

**GPS位置信息读取**

**1. 学习目标**

本次课程我们主要学习使用arduino和GPS模块实现位置信息读取功能。

**2. 课前准备**

GPS模块采用的是UART和USB通讯，这里使用arduino UNO的UART口读取信息，将模块的TX连接arduino UNO板子的D0引脚。VCC和GND分别连接5V和GND。

![img](../../en/03-arduino-position-read/images/1.png)

**3.** **程序**

初始化串口。

![img](../../en/03-arduino-position-read/images/2.jpg) 

将收到的数据打印输出。


**4. 编译下载程序**

4.1 我们需要通用Arduino IDE软件打开文件，然后点击菜单栏中的“√”编译程序，并且等待左下角出现“编译成功”的字样。

 ![img](../../en/03-arduino-position-read/images/3.jpg)

4.2 在Arduino IDE的菜单栏中，我们需要选择【工具】---【端口】---选择设备管理器中刚刚显示端口号，如下图所示。

![img](../../en/03-arduino-position-read/images/4.jpg) 

4.3 选择完成后，点击菜单栏下的“→”将代码上传到UNO板。 当左下角出现“上传完成”字样时，表示程序已成功上传到UNO板，如下图所示。

![img](../../en/03-arduino-position-read/images/5.jpg) 

 

**5. 实验现象**

模块通电后，需要32s左右的时间启动，之后模块上的串口打印状态灯会持续闪烁，此时可以正常接收数据。

程序下载后运行，打开串口监视窗口，打开串口软件，波特率设置为9600，串口会循环打印现在的位置信息，这些信息是没有处理过的原始信息，可以参照  [CASIC 协议规范](../../../docs/datasheets/CASIC-GNSS-protocol-spec-CN.pdf)  查看每条信息的具体内容。

![img](../../en/03-arduino-position-read/images/6.jpg) 

注意，模块天线需要在室外，否则可能搜索不到GPS信号。