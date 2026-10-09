[English](../../en/05-stm32f103/gps-parse-output.md) | [Deutsch](../../de/05-stm32f103/gps-parse-output.md) | [Español](../../es/05-stm32f103/gps-parse-output.md) | [Français](../../fr/05-stm32f103/gps-parse-output.md) | [Italiano](../../it/05-stm32f103/gps-parse-output.md) | 日本語 | [한국어](../../ko/05-stm32f103/gps-parse-output.md) | [Português (BR)](../../pt-br/05-stm32f103/gps-parse-output.md) | [Português (PT)](../../pt-pt/05-stm32f103/gps-parse-output.md) | [简体中文](../../zh-hans/05-stm32f103/gps-parse-output.md) | [繁體中文](../../zh-hant/05-stm32f103/gps-parse-output.md)

**GPS データのパースと出力（STM32）**

**1. 目的**

本レッスンでは、STM32F103C8T6 と GPS モジュールを使って測位情報をパースして出力します。

**2. 準備**

GPS モジュールは UART と USB で通信します。ここでは STM32 の UART を使用します。モジュールの TXD を STM32F103C8T6 ボードの PA10 ピンに、VCC と GND をボードの 5 V と GND に接続してください。TTL アダプタの GND と RXD を、STM32 の GND と PA9 に接続します。

![配線](../../en/05-stm32f103/images/1.png)

**3. プログラム**

モジュールのボーレートは 9600 です。

![コード](../../en/05-stm32f103/images/2.jpg)

受信データを読み取ってパースします。

![コード](../../en/05-stm32f103/images/3.jpg)

緯度・経度の単位を度に変換します。

![コード](../../en/05-stm32f103/images/4.jpg)

受信データをシリアルポート経由で出力します。

![コード](../../en/05-stm32f103/images/5.jpg)

注意：GPS／北斗の緯度・経度は単純な 100 倍の関係ではなく、度分変換が必要です。たとえば緯度 `2429.53531` N、経度 `11810.78036` E の場合：

```
24 + (29.53531 / 60) ≈ 24.49225517
118 + (10.78036 / 60) ≈ 118.17967267
```

また、マイコンの種類によっては、データ変換の精度により小さな誤差が生じることがあります。

**4. 結果**

電源投入後、モジュールが起動するまでに約 32 秒かかります。その後はシリアルステータス LED が点滅し続け、データを正常に受信できるようになります。

プログラムを書き込んで実行し、シリアルターミナルを 9600 baud で開くと、現在の測位情報が繰り返し出力されます。

![シリアル出力](../../en/05-stm32f103/images/6.jpg)

なお、モジュールのアンテナは屋外に設置する必要があります。屋内では GPS 信号を捕捉できないことがあります。
