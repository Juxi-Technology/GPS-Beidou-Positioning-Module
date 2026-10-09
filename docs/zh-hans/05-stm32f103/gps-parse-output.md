[English](../../en/05-stm32f103/gps-parse-output.md) | [Deutsch](../../de/05-stm32f103/gps-parse-output.md) | [Español](../../es/05-stm32f103/gps-parse-output.md) | [Français](../../fr/05-stm32f103/gps-parse-output.md) | [Italiano](../../it/05-stm32f103/gps-parse-output.md) | [日本語](../../ja/05-stm32f103/gps-parse-output.md) | [한국어](../../ko/05-stm32f103/gps-parse-output.md) | [Português (BR)](../../pt-br/05-stm32f103/gps-parse-output.md) | [Português (PT)](../../pt-pt/05-stm32f103/gps-parse-output.md) | 简体中文 | [繁體中文](../../zh-hant/05-stm32f103/gps-parse-output.md)

**GPS解析输出**

**1. 学习目标**

本次课程我们主要学习使用STM32F103C8T6和GPS模块模块实现位置信息解析输出功能。

**2. 课前准备**

GPS模块采用的是UART和USB通讯，这里使用STM32的UART口读取信息，将模块的TXD连接STM32F103C8T6板子的PA10引脚。VCC和GND分别连接STM32F103C8T6的5V和GND；TTL模块的GND和RXD分别与STM32的GND和PA9连接。

![img](../../en/05-stm32f103/images/1.png)

**3.** **程序**

模块的波特率为9600。

![img](../../en/05-stm32f103/images/2.jpg) 

读取并解析接收到的数据。

![img](../../en/05-stm32f103/images/3.jpg) 

将经纬度信息的单位转化为度

![img](../../en/05-stm32f103/images/4.jpg) 

通过串口打印接收到的数据。

![img](../../en/05-stm32f103/images/5.jpg) 

注意：其实GPS/北斗定位的坐标系值并不是简单的100倍关系，而是需要做一次度分秒的转换的。则我们获取的GPS/北斗坐标值，如北纬2429.53531，东经11810.78036，需要做如下计算：24+（29.53531/60）≈ 24.49225517 118+（10.78036/60）≈118.17967267。并且不同单片机可能存在数据转化精度的问题而存在一定误差。

**4. 实验现象**

模块通电后，需要32s左右的时间启动，之后模块上的串口打印状态灯会持续闪烁，此时可以正常接收数据。

程序下载后运行，打开串口软件，波特率设置为9600，串口会循环打印现在的位置信息。

![img](../../en/05-stm32f103/images/6.jpg) 

注意，模块天线需要在室外，否则可能搜索不到GPS信号。

 