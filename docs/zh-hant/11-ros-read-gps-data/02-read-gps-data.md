[English](../../en/11-ros-read-gps-data/02-read-gps-data.md) | [Deutsch](../../de/11-ros-read-gps-data/02-read-gps-data.md) | [Español](../../es/11-ros-read-gps-data/02-read-gps-data.md) | [Français](../../fr/11-ros-read-gps-data/02-read-gps-data.md) | [Italiano](../../it/11-ros-read-gps-data/02-read-gps-data.md) | [日本語](../../ja/11-ros-read-gps-data/02-read-gps-data.md) | [한국어](../../ko/11-ros-read-gps-data/02-read-gps-data.md) | [Português (BR)](../../pt-br/11-ros-read-gps-data/02-read-gps-data.md) | [Português (PT)](../../pt-pt/11-ros-read-gps-data/02-read-gps-data.md) | [简体中文](../../zh-hans/11-ros-read-gps-data/02-read-gps-data.md) | 繁體中文

### 讀取GPS模組資料

**該功能是透過終端機讀取GPS模組資料以及解析GPS資料得到經緯度和海拔資料。**

#### 1、透過終端機讀取GPS資料

終端機輸入，

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

![img_20260611114313](../../en/11-ros-read-gps-data/images/1.png)

然後我們查看下話題資料，終端機輸入，

```
ros2 topic list
```

![img_20260611114355](../../en/11-ros-read-gps-data/images/2.png)

關於GPS這幾個話題的資料，這裡做個說明，

| 話題            | 類型                       | 說明                                |
| --------------- | -------------------------- | ----------------------------------- |
| /extend_fix     | gps_common/GPSFix          | GPSFix訊息包含GPS衛星狀態和定位資訊 |
| /fix            | sensor_msgs/NavSatFix      | GPS定位資訊                         |
| /time_reference | sensor_msgs/TimeReferencd  | GPS時間資訊                         |
| /vel            | geometry_msgs/TwistStamped | GPS的速度資訊                       |

各個話題訊息類型可以參考以官網網址，

[sensor_msgs/NavSatFix Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/NavSatFix.html)

[sensor_msgs/TimeReference Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/TimeReference.html)

[geometry_msgs/TwistStamped Documentation (ros.org)](http://docs.ros.org/en/api/geometry_msgs/html/msg/TwistStamped.html)

我們可以在在終端機列印出這些話題訊息，得到的就是GPS資料，以列印/fix為例，終端機輸入

```
ros2 topic echo /fix
```

終端機會列印出以下資料，

![img_20260611114507](../../en/11-ros-read-gps-data/images/3.png)

其中，latitude，longitude，altitude分別代表的是緯度、經度和海拔。

#### 2、讀取GPS資料的經緯度和海拔

終端機執行，

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

在另一個終端機執行，

```
ros2 run nmea_navsat_driver read_lat_long.py 
```

![img_20260611114724](../../en/11-ros-read-gps-data/images/4.png)

終端機列印的資料就是當前GPS模組的經緯度和海拔，看看原始碼，read_lat_long.py

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

程式訂閱了/fix話題的資料，然後在回呼函式裡邊做了解析，最終列印到終端機上。
