[English](../../en/03-arduino-position-read/position-read.md) | [Deutsch](../../de/03-arduino-position-read/position-read.md) | [Español](../../es/03-arduino-position-read/position-read.md) | [Français](../../fr/03-arduino-position-read/position-read.md) | [Italiano](../../it/03-arduino-position-read/position-read.md) | [日本語](../../ja/03-arduino-position-read/position-read.md) | [한국어](../../ko/03-arduino-position-read/position-read.md) | [Português (BR)](../../pt-br/03-arduino-position-read/position-read.md) | [Português (PT)](../../pt-pt/03-arduino-position-read/position-read.md) | [简体中文](../../zh-hans/03-arduino-position-read/position-read.md) | 繁體中文

**GPS位置資訊讀取**

**1. 學習目標**

本次課程我們主要學習使用arduino和GPS模組實現位置資訊讀取功能。

**2. 課前準備**

GPS模組採用的是UART和USB通訊，這裡使用arduino UNO的UART埠讀取資訊，將模組的TX連接到arduino UNO板子的D0引腳。VCC和GND分別連接5V和GND。

![img](../../en/03-arduino-position-read/images/1.png)

**3.** **程式**

初始化序列埠。

![img](../../en/03-arduino-position-read/images/2.jpg) 

將收到的資料列印輸出。


**4. 編譯下載程式**

4.1 我們需要通用Arduino IDE軟體開啟檔案，然後點擊選單列中的“√”編譯程式，並且等待左下角出現“編譯成功”的字樣。

 ![img](../../en/03-arduino-position-read/images/3.jpg)

4.2 在Arduino IDE的選單列中，我們需要選擇【工具】---【連接埠】---選擇裝置管理員中剛剛顯示的連接埠號，如下圖所示。

![img](../../en/03-arduino-position-read/images/4.jpg) 

4.3 選擇完成後，點擊選單列下的“→”將程式碼上傳到UNO板。 當左下角出現“上傳完成”字樣時，表示程式已成功上傳到UNO板，如下圖所示。

![img](../../en/03-arduino-position-read/images/5.jpg) 

 

**5. 實驗現象**

模組通電後，需要32s左右的時間啟動，之後模組上的序列埠列印狀態燈會持續閃爍，此時可以正常接收資料。

程式下載後執行，開啟序列埠監視視窗，開啟序列埠軟體，鮑率設定為9600，序列埠會循環列印現在的位置資訊，這些資訊是沒有處理過的原始資訊，可以參照  [CASIC 協定規範](../../../docs/datasheets/CASIC-GNSS-protocol-spec-CN.pdf)  查看每條資訊的具體內容。

![img](../../en/03-arduino-position-read/images/6.jpg) 

注意，模組天線需要在室外，否則可能搜尋不到GPS信號。