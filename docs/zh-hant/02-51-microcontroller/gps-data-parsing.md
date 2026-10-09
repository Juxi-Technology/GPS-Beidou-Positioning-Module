[English](../../en/02-51-microcontroller/gps-data-parsing.md) | [Deutsch](../../de/02-51-microcontroller/gps-data-parsing.md) | [Español](../../es/02-51-microcontroller/gps-data-parsing.md) | [Français](../../fr/02-51-microcontroller/gps-data-parsing.md) | [Italiano](../../it/02-51-microcontroller/gps-data-parsing.md) | [日本語](../../ja/02-51-microcontroller/gps-data-parsing.md) | [한국어](../../ko/02-51-microcontroller/gps-data-parsing.md) | [Português (BR)](../../pt-br/02-51-microcontroller/gps-data-parsing.md) | [Português (PT)](../../pt-pt/02-51-microcontroller/gps-data-parsing.md) | [简体中文](../../zh-hans/02-51-microcontroller/gps-data-parsing.md) | 繁體中文

**GPS資料解析**

**1. 學習目標**

本次課程我們主要學習使用STC89C52RC型號的51單片機和GPS模組實現位置資訊解析功能。

**2. 課前準備**

GPS模組採用的是UART和USB通訊，這裡使用C51的UART埠讀取資訊，將模組的TX連接到51板子的P3.0引腳。VCC和GND分別連接5V和GND。

![img](../../en/02-51-microcontroller/images/1.png)

**3.** **程式**

初始化序列埠和資料陣列

![img](../../en/02-51-microcontroller/images/2.jpg) 

讀取並解析接收到的資料。

![img](../../en/02-51-microcontroller/images/3.jpg) 

透過序列埠列印接收到的資料。

![img](../../en/02-51-microcontroller/images/4.jpg) 

**4****. 實驗現象**

模組通電後，需要32s左右的時間啟動，之後模組上的序列埠列印狀態燈會持續閃爍，此時可以正常接收資料。

程式下載後執行，開啟序列埠軟體，鮑率設定為9600，序列埠會循環列印現在的位置資訊。

![img](../../en/02-51-microcontroller/images/5.jpg) 

注意，模組天線需要在室外，否則可能搜尋不到GPS信號。