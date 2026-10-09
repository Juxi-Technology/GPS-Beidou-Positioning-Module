[English](../../en/11-ros-read-gps-data/02-read-gps-data.md) | [Deutsch](../../de/11-ros-read-gps-data/02-read-gps-data.md) | [Español](../../es/11-ros-read-gps-data/02-read-gps-data.md) | Français | [Italiano](../../it/11-ros-read-gps-data/02-read-gps-data.md) | [日本語](../../ja/11-ros-read-gps-data/02-read-gps-data.md) | [한국어](../../ko/11-ros-read-gps-data/02-read-gps-data.md) | [Português (BR)](../../pt-br/11-ros-read-gps-data/02-read-gps-data.md) | [Português (PT)](../../pt-pt/11-ros-read-gps-data/02-read-gps-data.md) | [简体中文](../../zh-hans/11-ros-read-gps-data/02-read-gps-data.md) | [繁體中文](../../zh-hant/11-ros-read-gps-data/02-read-gps-data.md)

### Lecture des données du module GPS

**Cette fonction lit les données GPS depuis un terminal et les analyse en latitude, longitude et altitude.**

#### 1. Lecture des données GPS depuis un terminal

Dans un terminal :

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

![lancement](../../en/11-ros-read-gps-data/images/1.png)

Examinez maintenant les topics :

```
ros2 topic list
```

![liste des topics](../../en/11-ros-read-gps-data/images/2.png)

Une remarque sur les topics GPS :

| Topic | Type | Description |
| --- | --- | --- |
| `/extend_fix` | `gps_common/GPSFix` | Message GPSFix contenant l'état des satellites et les informations de fix |
| `/fix` | `sensor_msgs/NavSatFix` | Informations de fix GPS |
| `/time_reference` | `sensor_msgs/TimeReference` | Informations de temps GPS |
| `/vel` | `geometry_msgs/TwistStamped` | Vitesse GPS |

Les définitions des messages sont documentées à l'adresse :

[sensor_msgs/NavSatFix Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/NavSatFix.html)

[sensor_msgs/TimeReference Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/TimeReference.html)

[geometry_msgs/TwistStamped Documentation (ros.org)](http://docs.ros.org/en/api/geometry_msgs/html/msg/TwistStamped.html)

Vous pouvez afficher ces messages de topic dans un terminal — ce que vous obtenez, ce sont les données GPS. Par exemple, pour afficher `/fix` :

```
ros2 topic echo /fix
```

Le terminal affiche :

![echo fix](../../en/11-ros-read-gps-data/images/3.png)

Ici, `latitude`, `longitude` et `altitude` sont la latitude, la longitude et l'altitude.

#### 2. Lecture de la latitude, de la longitude et de l'altitude

Dans un terminal :

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

Dans un autre terminal :

```
ros2 run nmea_navsat_driver read_lat_long.py
```

![lecture lat long](../../en/11-ros-read-gps-data/images/4.png)

Les données affichées correspondent à la latitude, la longitude et l'altitude actuelles. Jetez un œil au code source, `read_lat_long.py` :

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

Le programme s'abonne à `/fix`, analyse le message dans la fonction de rappel et l'affiche dans le terminal.
