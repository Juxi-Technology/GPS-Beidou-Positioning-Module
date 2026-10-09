[English](../../en/03-arduino-position-read/position-read.md) | [Deutsch](../../de/03-arduino-position-read/position-read.md) | [Español](../../es/03-arduino-position-read/position-read.md) | [Français](../../fr/03-arduino-position-read/position-read.md) | [Italiano](../../it/03-arduino-position-read/position-read.md) | 日本語 | [한국어](../../ko/03-arduino-position-read/position-read.md) | [Português (BR)](../../pt-br/03-arduino-position-read/position-read.md) | [Português (PT)](../../pt-pt/03-arduino-position-read/position-read.md) | [简体中文](../../zh-hans/03-arduino-position-read/position-read.md) | [繁體中文](../../zh-hant/03-arduino-position-read/position-read.md)

**GPS 測位データの読み取り**

**1. 目的**

本レッスンでは、Arduino と GPS モジュールを使って測位情報を読み取ります。

**2. 準備**

GPS モジュールは UART と USB で通信します。ここでは Arduino UNO の UART を使用します。モジュールの TX を UNO の D0 ピンに、VCC と GND を 5 V と GND に接続してください。

![配線](../../en/03-arduino-position-read/images/1.png)

**3. プログラム**

シリアルポートを初期化します。

![コード](../../en/03-arduino-position-read/images/2.jpg)

受信データを出力します。

**4. コンパイルと書き込み**

4.1 Arduino IDE でファイルを開き、ツールバーの「✓」ボタンをクリックしてコンパイルし、ステータスバーに「Done compiling」と表示されるまで待ちます。

![コンパイル](../../en/03-arduino-position-read/images/3.jpg)

4.2 Arduino IDE のメニューで「ツール」→「ポート」→ デバイスマネージャーに表示されているポートを選択します（以下を参照）。

![ポートの選択](../../en/03-arduino-position-read/images/4.jpg)

4.3 次に「→」ボタンをクリックして、コードを UNO ボードへ書き込みます。「Done uploading」と表示されれば書き込み成功です。

![書き込み](../../en/03-arduino-position-read/images/5.jpg)

**5. 結果**

電源投入後、モジュールが起動するまでに約 32 秒かかります。その後はシリアルステータス LED が点滅し続け、データを正常に受信できるようになります。

プログラムを実行し、シリアルモニタを開いてボーレートを 9600 に設定すると、現在の測位情報が繰り返し出力されます。これは未処理の生データです。各センテンスの意味については、[CASIC GNSS プロトコル仕様書](../../../docs/datasheets/CASIC-GNSS-protocol-spec-CN.pdf)を参照してください。

![シリアル出力](../../en/03-arduino-position-read/images/6.jpg)

なお、モジュールのアンテナは屋外に設置する必要があります。屋内では GPS 信号を捕捉できないことがあります。
