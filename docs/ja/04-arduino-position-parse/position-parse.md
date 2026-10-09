[English](../../en/04-arduino-position-parse/position-parse.md) | [Deutsch](../../de/04-arduino-position-parse/position-parse.md) | [Español](../../es/04-arduino-position-parse/position-parse.md) | [Français](../../fr/04-arduino-position-parse/position-parse.md) | [Italiano](../../it/04-arduino-position-parse/position-parse.md) | 日本語 | [한국어](../../ko/04-arduino-position-parse/position-parse.md) | [Português (BR)](../../pt-br/04-arduino-position-parse/position-parse.md) | [Português (PT)](../../pt-pt/04-arduino-position-parse/position-parse.md) | [简体中文](../../zh-hans/04-arduino-position-parse/position-parse.md) | [繁體中文](../../zh-hant/04-arduino-position-parse/position-parse.md)

**GPS 測位データのパース**

**1. 目的**

本レッスンでは、Arduino と GPS モジュールを使って測位情報をパースして出力します。

**2. 準備**

GPS モジュールは UART と USB で通信します。ここでは Arduino UNO の UART を使用します。モジュールの TX を UNO の D0 ピンに、VCC と GND を 5 V と GND に接続してください。

![配線](../../en/04-arduino-position-parse/images/1.png)

**3. プログラム**

シリアルポートを初期化します。

![コード](../../en/04-arduino-position-parse/images/2.jpg)

シリアルデータを読み取ります。

![コード](../../en/04-arduino-position-parse/images/3.jpg)

シリアルデータをパースします。

![コード](../../en/04-arduino-position-parse/images/4.jpg)

パースした測位情報を出力します。

![コード](../../en/04-arduino-position-parse/images/5.jpg)

**4. コンパイルと書き込み**

4.1 Arduino IDE でファイルを開き、「✓」ボタンをクリックしてコンパイルし、「Done compiling」と表示されるまで待ちます。

![コンパイル](../../en/04-arduino-position-parse/images/6.jpg)

4.2 メニューで「ツール」→「ポート」→ デバイスマネージャーに表示されているポートを選択します。

![ポートの選択](../../en/04-arduino-position-parse/images/7.jpg)

4.3 「→」ボタンをクリックして書き込みます。「Done uploading」と表示されれば書き込み成功です。

![書き込み](../../en/04-arduino-position-parse/images/8.jpg)

**5. 結果**

電源投入後、モジュールが起動するまでに約 32 秒かかります。その後はシリアルステータス LED が点滅し続け、データを正常に受信できるようになります。

プログラムを実行し、シリアルモニタを 9600 baud で開くと、パースされたリアルタイムの測位情報が繰り返し出力されます。

![シリアル出力](../../en/04-arduino-position-parse/images/9.jpg)

なお、モジュールのアンテナは屋外に設置する必要があります。屋内では GPS 信号を捕捉できないことがあります。
