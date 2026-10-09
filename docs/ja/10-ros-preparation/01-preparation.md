[English](../../en/10-ros-preparation/01-preparation.md) | [Deutsch](../../de/10-ros-preparation/01-preparation.md) | [Español](../../es/10-ros-preparation/01-preparation.md) | [Français](../../fr/10-ros-preparation/01-preparation.md) | [Italiano](../../it/10-ros-preparation/01-preparation.md) | 日本語 | [한국어](../../ko/10-ros-preparation/01-preparation.md) | [Português (BR)](../../pt-br/10-ros-preparation/01-preparation.md) | [Português (PT)](../../pt-pt/10-ros-preparation/01-preparation.md) | [简体中文](../../zh-hans/10-ros-preparation/01-preparation.md) | [繁體中文](../../zh-hant/10-ros-preparation/01-preparation.md)

### はじめに

#### 1. GPS パッケージのビルド

(1) ワークスペースを作成し、`gps_src` フォルダの内容をワークスペースの `src` ディレクトリにコピーしてから、`colcon build` でビルドします。エラーが表示されなければビルド成功です。

`~/gps_ros2` 内で：

```
colcon build
```

続いて `~/gps_ros2` 内で：

```
source install/setup.bash
```

(2) 各パッケージの内容：

- `nmea_navsat_driver` — GPS モジュールの起動、データの読み取り、GPS 軌跡の描画
- `nmea_msgs` — GPS 関連メッセージのメッセージ定義
- `imu_gps_localization` — IMU と GPS データの融合
- `gps_goal` — 緯度・経度を Nav2 のゴールに変換

#### 2. GPS モジュールへの固定ポートの割り当て

GPS モジュールはシリアルポート経由で PC またはホストと通信するため、固定のポート名を割り当てます。そうしないと、ポート番号が変わるたびにホストがモジュールを見つけられなくなることがあります。

(1) 接続されている USB デバイスを一覧表示し、GPS モジュールを特定します。**lsusb** を実行し、以下に示すようにデバイス ID を確認します。

![lsusb の出力](../../en/10-ros-preparation/images/1.png)

(2) デバイス ID がわかったら、udev ルールファイルを書いてポートを割り当てます。次を実行します：

```
sudo gedit /etc/udev/rules.d/my_serial.rules
```

そして以下を貼り付けます：

```
KERNEL=="ttyUSB*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", MODE:="0777", SYMLINK+="myserial"
```

保存して終了し、実行可能にします：

```
sudo chmod 777 /etc/udev/rules.d/my_serial.rules
```

(3) GPS モジュールを抜き差しし、`ll /dev/myserial` を実行して割り当てが機能したか確認します。以下の出力が得られれば成功です。

```
ll /dev/myserial
```

![udev の割り当て](../../en/10-ros-preparation/images/2.png)
