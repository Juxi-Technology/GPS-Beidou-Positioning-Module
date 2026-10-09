[English](../../en/11-ros-read-gps-data/02-read-gps-data.md) | [Deutsch](../../de/11-ros-read-gps-data/02-read-gps-data.md) | [Español](../../es/11-ros-read-gps-data/02-read-gps-data.md) | [Français](../../fr/11-ros-read-gps-data/02-read-gps-data.md) | [Italiano](../../it/11-ros-read-gps-data/02-read-gps-data.md) | [日本語](../../ja/11-ros-read-gps-data/02-read-gps-data.md) | [한국어](../../ko/11-ros-read-gps-data/02-read-gps-data.md) | [Português (BR)](../../pt-br/11-ros-read-gps-data/02-read-gps-data.md) | [Português (PT)](../../pt-pt/11-ros-read-gps-data/02-read-gps-data.md) | 简体中文 | [繁體中文](../../zh-hant/11-ros-read-gps-data/02-read-gps-data.md)

### 读取GPS模块数据

**该功能是通过终端读取GPS模块数据以及解析GPS数据得到经纬度和海拔数据。**

#### 1、通过终端读取GPS数据

终端输入，

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

![img_20260611114313](../../en/11-ros-read-gps-data/images/1.png)

然后我们查看下话题数据，终端输入，

```
ros2 topic list
```

![img_20260611114355](../../en/11-ros-read-gps-data/images/2.png)

关于GPS这几个话题的数据，这里做个说明，

| 话题            | 类型                       | 说明                                |
| --------------- | -------------------------- | ----------------------------------- |
| /extend_fix     | gps_common/GPSFix          | GPSFix消息包含GPS卫星状态和定位信息 |
| /fix            | sensor_msgs/NavSatFix      | GPS定位信息                         |
| /time_reference | sensor_msgs/TimeReferencd  | GPS时间信息                         |
| /vel            | geometry_msgs/TwistStamped | GPS的速度信息                       |

各个话题消息类型可以参考以官网网址，

[sensor_msgs/NavSatFix Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/NavSatFix.html)

[sensor_msgs/TimeReference Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/TimeReference.html)

[geometry_msgs/TwistStamped Documentation (ros.org)](http://docs.ros.org/en/api/geometry_msgs/html/msg/TwistStamped.html)

我们可以在在终端打印出这些话题消息，得到的就是GPS数据，以打印/fix为例，终端输入

```
ros2 topic echo /fix
```

终端会打印出以下数据，

![img_20260611114507](../../en/11-ros-read-gps-data/images/3.png)

其中，latitude，longitude，altitude分别代表的是纬度、经度和海拔。

#### 2、读取GPS数据的经纬度和海拔

终端运行，

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

在另一个终端运行，

```
ros2 run nmea_navsat_driver read_lat_long.py 
```

![img_20260611114724](../../en/11-ros-read-gps-data/images/4.png)

终端打印的数据就是当前GPS模块的经纬度和海拔，看看源码，read_lat_long.py

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

程序订阅了/fix话题的数据，然后在回调函数里边做了解析，最终打印到终端上。
