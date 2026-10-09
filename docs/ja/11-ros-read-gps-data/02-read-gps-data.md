[English](../../en/11-ros-read-gps-data/02-read-gps-data.md) | [Deutsch](../../de/11-ros-read-gps-data/02-read-gps-data.md) | [Español](../../es/11-ros-read-gps-data/02-read-gps-data.md) | [Français](../../fr/11-ros-read-gps-data/02-read-gps-data.md) | [Italiano](../../it/11-ros-read-gps-data/02-read-gps-data.md) | 日本語 | [한국어](../../ko/11-ros-read-gps-data/02-read-gps-data.md) | [Português (BR)](../../pt-br/11-ros-read-gps-data/02-read-gps-data.md) | [Português (PT)](../../pt-pt/11-ros-read-gps-data/02-read-gps-data.md) | [简体中文](../../zh-hans/11-ros-read-gps-data/02-read-gps-data.md) | [繁體中文](../../zh-hant/11-ros-read-gps-data/02-read-gps-data.md)

### GPS モジュールデータの読み取り

**この機能は、ターミナルから GPS データを読み取り、緯度・経度・高度にパースします。**

#### 1. ターミナルからの GPS データの読み取り

ターミナルで：

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

![launch](../../en/11-ros-read-gps-data/images/1.png)

次にトピックを確認します：

```
ros2 topic list
```

![トピック一覧](../../en/11-ros-read-gps-data/images/2.png)

GPS トピックに関する補足：

| トピック | 型 | 説明 |
| --- | --- | --- |
| `/extend_fix` | `gps_common/GPSFix` | 衛星の状態と測位情報を含む GPSFix メッセージ |
| `/fix` | `sensor_msgs/NavSatFix` | GPS 測位情報 |
| `/time_reference` | `sensor_msgs/TimeReference` | GPS 時刻情報 |
| `/vel` | `geometry_msgs/TwistStamped` | GPS 速度 |

メッセージ定義は次のドキュメントに記載されています：

[sensor_msgs/NavSatFix Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/NavSatFix.html)

[sensor_msgs/TimeReference Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/TimeReference.html)

[geometry_msgs/TwistStamped Documentation (ros.org)](http://docs.ros.org/en/api/geometry_msgs/html/msg/TwistStamped.html)

これらのトピックメッセージはターミナルに出力できます。得られるものが GPS データです。たとえば `/fix` を出力するには：

```
ros2 topic echo /fix
```

ターミナルには次のように出力されます：

![echo fix](../../en/11-ros-read-gps-data/images/3.png)

ここで `latitude`、`longitude`、`altitude` はそれぞれ緯度、経度、高度です。

#### 2. 緯度・経度・高度の読み取り

ターミナルで：

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

もう 1 つのターミナルで：

```
ros2 run nmea_navsat_driver read_lat_long.py
```

![read lat long](../../en/11-ros-read-gps-data/images/4.png)

出力されるデータが現在の緯度・経度・高度です。ソース `read_lat_long.py` を見てみましょう：

```python
#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix

class GPSSubscriber(Node):
    def __init__(self):
        super().__init__('GPS_subscriber')
        self.subscription = self.create_subscription(
            NavSatFix,
            '/fix',
            self.gps_callback,
            10)
        self.subscription

    def gps_callback(self, msg):
        self.get_logger().info(f"latitude:{msg.latitude:.6f}, longitude:{msg.longitude:.6f}, altitude:{msg.altitude:.6f}")

def main(args=None):
    rclpy.init(args=args)
    gps_subscriber = GPSSubscriber()
    rclpy.spin(gps_subscriber)
    gps_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

プログラムは `/fix` を購読し、コールバックでメッセージをパースしてターミナルに出力します。
