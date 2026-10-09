[English](../../en/08-raspberry-pi-position-parse/position-parse.md) | [Deutsch](../../de/08-raspberry-pi-position-parse/position-parse.md) | [Español](../../es/08-raspberry-pi-position-parse/position-parse.md) | [Français](../../fr/08-raspberry-pi-position-parse/position-parse.md) | [Italiano](../../it/08-raspberry-pi-position-parse/position-parse.md) | [日本語](../../ja/08-raspberry-pi-position-parse/position-parse.md) | [한국어](../../ko/08-raspberry-pi-position-parse/position-parse.md) | [Português (BR)](../../pt-br/08-raspberry-pi-position-parse/position-parse.md) | [Português (PT)](../../pt-pt/08-raspberry-pi-position-parse/position-parse.md) | [简体中文](../../zh-hans/08-raspberry-pi-position-parse/position-parse.md) | 繁體中文

**GPS模組解析位置資訊**

**1. 學習目標**

本次課程我們主要學習使用樹莓派和GPS模組實讀取並解析位置資訊。

**2. 課前準備**

GPS模組採用的是UART通訊或USB通訊，這裡以USB通訊為例。

![img](../../en/08-raspberry-pi-position-parse/images/1.png)

使用type-c線連接樹莓派和GPS模組，執行命令 ls /dev | grep 'ttyUSB' ，可以看到辨識到語音模組為USB0

![img](../../en/08-raspberry-pi-position-parse/images/2.jpg) 

**3. 程式**

本次課程的程式請參考：GPS.py

初始化USB：

![img](../../en/08-raspberry-pi-position-parse/images/3.jpg) 

位置資訊取得和解析函式，下圖中在位置資訊中篩選出GNGGA開頭的位置資訊，然後解析出資料存到各個全域變數中。

![img](../../en/08-raspberry-pi-position-parse/images/4.jpg) 

![img](../../en/08-raspberry-pi-position-parse/images/5.jpg) 

同樣的方法取得了GNVTG的航向資訊並解析。

![img](../../en/08-raspberry-pi-position-parse/images/6.jpg) 

解析後的資料循環列印

![img](../../en/08-raspberry-pi-position-parse/images/7.jpg) 

**4. 執行程式**

終端機輸入sudo python2 GPS.py執行程式。

**5.** **實驗現象**

模組通電後，需要32s左右的時間啟動，之後模組上的序列埠列印狀態燈會持續閃爍，此時可以正常接收資料。

程式執行以後，開始初始化USB，初始化成功顯示“GPS Serial Opened! Baudrate=9600”，否則顯示“GPS Serial Open Failed!”，如果錯誤需要檢查接線或USB埠，之後循環列印位置和航向資訊。

![img](../../en/08-raspberry-pi-position-parse/images/8.jpg) 

按Ctrl+C結束資訊讀取。

注意，模組天線需要在室外，否則可能搜尋不到GPS信號，搜尋不到信號的時候列印"GPS no found"。