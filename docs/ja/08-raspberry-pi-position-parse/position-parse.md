[English](../../en/08-raspberry-pi-position-parse/position-parse.md) | [Deutsch](../../de/08-raspberry-pi-position-parse/position-parse.md) | [Español](../../es/08-raspberry-pi-position-parse/position-parse.md) | [Français](../../fr/08-raspberry-pi-position-parse/position-parse.md) | [Italiano](../../it/08-raspberry-pi-position-parse/position-parse.md) | 日本語 | [한국어](../../ko/08-raspberry-pi-position-parse/position-parse.md) | [Português (BR)](../../pt-br/08-raspberry-pi-position-parse/position-parse.md) | [Português (PT)](../../pt-pt/08-raspberry-pi-position-parse/position-parse.md) | [简体中文](../../zh-hans/08-raspberry-pi-position-parse/position-parse.md) | [繁體中文](../../zh-hant/08-raspberry-pi-position-parse/position-parse.md)

**GPS 測位データの読み取りとパース（Raspberry Pi）**

**1. 目的**

本レッスンでは、Raspberry Pi と GPS モジュールを使って測位情報を読み取ってパースします。

**2. 準備**

GPS モジュールは UART または USB による通信に対応しています。ここでは USB を使用します。

![モジュール](../../en/08-raspberry-pi-position-parse/images/1.png)

Type-C ケーブルで Raspberry Pi と GPS モジュールを接続し、`ls /dev | grep 'ttyUSB'` を実行します。モジュールは `USB0` として検出されます。

![デバイスの検出](../../en/08-raspberry-pi-position-parse/images/2.jpg)

**3. プログラム**

本レッスンのプログラムは `GPS.py` です。

USB を初期化します：

![コード](../../en/08-raspberry-pi-position-parse/images/3.jpg)

測位情報の取得・パース関数は、受信データから `GNGGA` で始まるセンテンスを抽出し、グローバル変数にパースします。

![コード](../../en/08-raspberry-pi-position-parse/images/4.jpg)

![コード](../../en/08-raspberry-pi-position-parse/images/5.jpg)

同様の方法で、`GNVTG` から方位情報を読み取ってパースします。

![コード](../../en/08-raspberry-pi-position-parse/images/6.jpg)

パースしたデータを繰り返し出力します。

![コード](../../en/08-raspberry-pi-position-parse/images/7.jpg)

**4. プログラムの実行**

ターミナルで `sudo python2 GPS.py` を実行します。

**5. 結果**

電源投入後、モジュールが起動するまでに約 32 秒かかります。その後はシリアルステータス LED が点滅し続け、データを正常に受信できるようになります。

プログラムが起動すると USB を初期化し、成功時は `GPS Serial Opened! Baudrate=9600`、失敗時は `GPS Serial Open Failed!` を出力します。失敗した場合は配線または USB ポートを確認してください。その後、測位情報と方位情報を繰り返し出力します。

![出力](../../en/08-raspberry-pi-position-parse/images/8.jpg)

Ctrl+C を押すと読み取りを停止します。

なお、モジュールのアンテナは屋外に設置する必要があります。屋内では GPS 信号を捕捉できないことがあります。信号が見つからない場合は `GPS no found` を出力します。
