[English](../../en/11-ros-read-gps-data/02-read-gps-data.md) | [Deutsch](../../de/11-ros-read-gps-data/02-read-gps-data.md) | [Español](../../es/11-ros-read-gps-data/02-read-gps-data.md) | [Français](../../fr/11-ros-read-gps-data/02-read-gps-data.md) | Italiano | [日本語](../../ja/11-ros-read-gps-data/02-read-gps-data.md) | [한국어](../../ko/11-ros-read-gps-data/02-read-gps-data.md) | [Português (BR)](../../pt-br/11-ros-read-gps-data/02-read-gps-data.md) | [Português (PT)](../../pt-pt/11-ros-read-gps-data/02-read-gps-data.md) | [简体中文](../../zh-hans/11-ros-read-gps-data/02-read-gps-data.md) | [繁體中文](../../zh-hant/11-ros-read-gps-data/02-read-gps-data.md)

### Lettura dei dati del modulo GPS

**Questa funzione legge i dati GPS da un terminale e li analizza in latitudine, longitudine e altitudine.**

#### 1. Lettura dei dati GPS da un terminale

In un terminale:

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

![launch](../../en/11-ros-read-gps-data/images/1.png)

Ora esaminare i topic:

```
ros2 topic list
```

![elenco dei topic](../../en/11-ros-read-gps-data/images/2.png)

Una nota sui topic GPS:

| Topic | Tipo | Descrizione |
| --- | --- | --- |
| `/extend_fix` | `gps_common/GPSFix` | Messaggio GPSFix contenente lo stato dei satelliti e le informazioni di fix |
| `/fix` | `sensor_msgs/NavSatFix` | Informazioni di fix GPS |
| `/time_reference` | `sensor_msgs/TimeReference` | Informazioni sull'ora GPS |
| `/vel` | `geometry_msgs/TwistStamped` | Velocità GPS |

Le definizioni dei messaggi sono documentate all'indirizzo:

[sensor_msgs/NavSatFix Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/NavSatFix.html)

[sensor_msgs/TimeReference Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/TimeReference.html)

[geometry_msgs/TwistStamped Documentation (ros.org)](http://docs.ros.org/en/api/geometry_msgs/html/msg/TwistStamped.html)

È possibile stampare i messaggi di questi topic in un terminale — ciò che si ottiene sono i dati GPS. Ad esempio, per stampare `/fix`:

```
ros2 topic echo /fix
```

Il terminale stampa:

![echo fix](../../en/11-ros-read-gps-data/images/3.png)

Qui `latitude`, `longitude` e `altitude` sono la latitudine, la longitudine e l'altitudine.

#### 2. Lettura di latitudine, longitudine e altitudine

In un terminale:

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

In un altro terminale:

```
ros2 run nmea_navsat_driver read_lat_long.py
```

![lettura lat long](../../en/11-ros-read-gps-data/images/4.png)

I dati stampati sono la latitudine, la longitudine e l'altitudine correnti. Dare un'occhiata al sorgente, `read_lat_long.py`:

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

Il programma si sottoscrive a `/fix`, analizza il messaggio nella callback e lo stampa sul terminale.
