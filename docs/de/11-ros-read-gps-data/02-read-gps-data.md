[English](../../en/11-ros-read-gps-data/02-read-gps-data.md) | Deutsch | [Español](../../es/11-ros-read-gps-data/02-read-gps-data.md) | [Français](../../fr/11-ros-read-gps-data/02-read-gps-data.md) | [Italiano](../../it/11-ros-read-gps-data/02-read-gps-data.md) | [日本語](../../ja/11-ros-read-gps-data/02-read-gps-data.md) | [한국어](../../ko/11-ros-read-gps-data/02-read-gps-data.md) | [Português (BR)](../../pt-br/11-ros-read-gps-data/02-read-gps-data.md) | [Português (PT)](../../pt-pt/11-ros-read-gps-data/02-read-gps-data.md) | [简体中文](../../zh-hans/11-ros-read-gps-data/02-read-gps-data.md) | [繁體中文](../../zh-hant/11-ros-read-gps-data/02-read-gps-data.md)

### GPS-Moduldaten lesen

**Diese Funktion liest GPS-Daten aus einem Terminal und wertet sie in Breiten- und Längengrad sowie Höhe aus.**

#### 1. GPS-Daten aus einem Terminal lesen

In einem Terminal:

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

![Start](../../en/11-ros-read-gps-data/images/1.png)

Betrachten Sie nun die Topics:

```
ros2 topic list
```

![Topic-Liste](../../en/11-ros-read-gps-data/images/2.png)

Ein Hinweis zu den GPS-Topics:

| Topic | Typ | Beschreibung |
| --- | --- | --- |
| `/extend_fix` | `gps_common/GPSFix` | GPSFix-Nachricht mit Satellitenstatus und Fix-Informationen |
| `/fix` | `sensor_msgs/NavSatFix` | GPS-Fix-Informationen |
| `/time_reference` | `sensor_msgs/TimeReference` | GPS-Zeitinformationen |
| `/vel` | `geometry_msgs/TwistStamped` | GPS-Geschwindigkeit |

Die Nachrichtendefinitionen sind dokumentiert unter:

[sensor_msgs/NavSatFix Dokumentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/NavSatFix.html)

[sensor_msgs/TimeReference Dokumentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/TimeReference.html)

[geometry_msgs/TwistStamped Dokumentation (ros.org)](http://docs.ros.org/en/api/geometry_msgs/html/msg/TwistStamped.html)

Sie können diese Topic-Nachrichten in einem Terminal ausgeben — was Sie erhalten, sind die GPS-Daten. Um beispielsweise `/fix` auszugeben:

```
ros2 topic echo /fix
```

Das Terminal gibt aus:

![Fix ausgeben](../../en/11-ros-read-gps-data/images/3.png)

Hier sind `latitude`, `longitude` und `altitude` der Breitengrad, der Längengrad und die Höhe.

#### 2. Breiten- und Längengrad sowie Höhe lesen

In einem Terminal:

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

In einem anderen Terminal:

```
ros2 run nmea_navsat_driver read_lat_long.py
```

![Breite Länge lesen](../../en/11-ros-read-gps-data/images/4.png)

Die ausgegebenen Daten sind der aktuelle Breiten- und Längengrad sowie die Höhe. Werfen Sie einen Blick in den Quellcode `read_lat_long.py`:

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

Das Programm abonniert `/fix`, wertet die Nachricht im Callback aus und gibt sie im Terminal aus.
