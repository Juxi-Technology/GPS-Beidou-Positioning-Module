[English](../../en/05-stm32f103/gps-parse-output.md) | [Deutsch](../../de/05-stm32f103/gps-parse-output.md) | [Español](../../es/05-stm32f103/gps-parse-output.md) | [Français](../../fr/05-stm32f103/gps-parse-output.md) | [Italiano](../../it/05-stm32f103/gps-parse-output.md) | [日本語](../../ja/05-stm32f103/gps-parse-output.md) | [한국어](../../ko/05-stm32f103/gps-parse-output.md) | [Português (BR)](../../pt-br/05-stm32f103/gps-parse-output.md) | [Português (PT)](../../pt-pt/05-stm32f103/gps-parse-output.md) | [简体中文](../../zh-hans/05-stm32f103/gps-parse-output.md) | 繁體中文

**GPS解析輸出**

**1. 學習目標**

本次課程我們主要學習使用STM32F103C8T6和GPS模組模組實現位置資訊解析輸出功能。

**2. 課前準備**

GPS模組採用的是UART和USB通訊，這裡使用STM32的UART埠讀取資訊，將模組的TXD連接到STM32F103C8T6板子的PA10引腳。VCC和GND分別連接STM32F103C8T6的5V和GND；TTL模組的GND和RXD分別與STM32的GND和PA9連接。

![img](../../en/05-stm32f103/images/1.png)

**3.** **程式**

模組的鮑率為9600。

![img](../../en/05-stm32f103/images/2.jpg) 

讀取並解析接收到的資料。

![img](../../en/05-stm32f103/images/3.jpg) 

將經緯度資訊的單位轉換為度

![img](../../en/05-stm32f103/images/4.jpg) 

透過序列埠列印接收到的資料。

![img](../../en/05-stm32f103/images/5.jpg) 

注意：其實GPS/北斗定位的座標系值並不是簡單的100倍關係，而是需要做一次度分秒的轉換的。則我們取得的GPS/北斗座標值，如北緯2429.53531，東經11810.78036，需要做如下計算：24+（29.53531/60）≈ 24.49225517 118+（10.78036/60）≈118.17967267。並且不同單片機可能存在資料轉換精度的問題而存在一定誤差。

**4. 實驗現象**

模組通電後，需要32s左右的時間啟動，之後模組上的序列埠列印狀態燈會持續閃爍，此時可以正常接收資料。

程式下載後執行，開啟序列埠軟體，鮑率設定為9600，序列埠會循環列印現在的位置資訊。

![img](../../en/05-stm32f103/images/6.jpg) 

注意，模組天線需要在室外，否則可能搜尋不到GPS信號。

 