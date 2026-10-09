[English](../../en/11-ros-read-gps-data/02-read-gps-data.md) | [Deutsch](../../de/11-ros-read-gps-data/02-read-gps-data.md) | [Español](../../es/11-ros-read-gps-data/02-read-gps-data.md) | [Français](../../fr/11-ros-read-gps-data/02-read-gps-data.md) | [Italiano](../../it/11-ros-read-gps-data/02-read-gps-data.md) | [日本語](../../ja/11-ros-read-gps-data/02-read-gps-data.md) | 한국어 | [Português (BR)](../../pt-br/11-ros-read-gps-data/02-read-gps-data.md) | [Português (PT)](../../pt-pt/11-ros-read-gps-data/02-read-gps-data.md) | [简体中文](../../zh-hans/11-ros-read-gps-data/02-read-gps-data.md) | [繁體中文](../../zh-hant/11-ros-read-gps-data/02-read-gps-data.md)

### GPS 모듈 데이터 읽기

**이 기능은 터미널에서 GPS 데이터를 읽어 위도, 경도, 고도로 파싱합니다.**

#### 1. 터미널에서 GPS 데이터 읽기

터미널에서:

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

![실행](../../en/11-ros-read-gps-data/images/1.png)

이제 토픽을 살펴봅니다:

```
ros2 topic list
```

![토픽 목록](../../en/11-ros-read-gps-data/images/2.png)

GPS 토픽에 대한 참고:

| 토픽 | 유형 | 설명 |
| --- | --- | --- |
| `/extend_fix` | `gps_common/GPSFix` | 위성 상태와 측위 정보를 담은 GPSFix 메시지 |
| `/fix` | `sensor_msgs/NavSatFix` | GPS 측위 정보 |
| `/time_reference` | `sensor_msgs/TimeReference` | GPS 시각 정보 |
| `/vel` | `geometry_msgs/TwistStamped` | GPS 속도 |

메시지 정의는 다음에 문서화되어 있습니다:

[sensor_msgs/NavSatFix Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/NavSatFix.html)

[sensor_msgs/TimeReference Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/TimeReference.html)

[geometry_msgs/TwistStamped Documentation (ros.org)](http://docs.ros.org/en/api/geometry_msgs/html/msg/TwistStamped.html)

터미널에서 이러한 토픽 메시지를 출력할 수 있으며, 출력되는 것이 바로 GPS 데이터입니다. 예를 들어 `/fix`를 출력하려면:

```
ros2 topic echo /fix
```

터미널에 출력됩니다:

![echo fix](../../en/11-ros-read-gps-data/images/3.png)

여기서 `latitude`, `longitude`, `altitude`는 각각 위도, 경도, 고도입니다.

#### 2. 위도, 경도, 고도 읽기

터미널에서:

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

다른 터미널에서:

```
ros2 run nmea_navsat_driver read_lat_long.py
```

![위도 경도 읽기](../../en/11-ros-read-gps-data/images/4.png)

출력된 데이터가 현재의 위도, 경도, 고도입니다. 소스 `read_lat_long.py`를 살펴보십시오:

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

이 프로그램은 `/fix`를 구독하고, 콜백에서 메시지를 파싱하여 터미널에 출력합니다.
