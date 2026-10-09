[English](../../en/11-ros-read-gps-data/02-read-gps-data.md) | [Deutsch](../../de/11-ros-read-gps-data/02-read-gps-data.md) | [Español](../../es/11-ros-read-gps-data/02-read-gps-data.md) | [Français](../../fr/11-ros-read-gps-data/02-read-gps-data.md) | [Italiano](../../it/11-ros-read-gps-data/02-read-gps-data.md) | [日本語](../../ja/11-ros-read-gps-data/02-read-gps-data.md) | [한국어](../../ko/11-ros-read-gps-data/02-read-gps-data.md) | [Português (BR)](../../pt-br/11-ros-read-gps-data/02-read-gps-data.md) | Português (PT) | [简体中文](../../zh-hans/11-ros-read-gps-data/02-read-gps-data.md) | [繁體中文](../../zh-hant/11-ros-read-gps-data/02-read-gps-data.md)

### Ler os Dados do Módulo GPS

**Esta funcionalidade lê os dados GPS a partir de um terminal e analisa-os em latitude, longitude e altitude.**

#### 1. Ler os dados GPS a partir de um terminal

Num terminal:

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

![arranque](../../en/11-ros-read-gps-data/images/1.png)

Agora, veja os tópicos:

```
ros2 topic list
```

![lista de tópicos](../../en/11-ros-read-gps-data/images/2.png)

Uma nota sobre os tópicos do GPS:

| Tópico | Tipo | Descrição |
| --- | --- | --- |
| `/extend_fix` | `gps_common/GPSFix` | Mensagem GPSFix com o estado dos satélites e a informação de fix |
| `/fix` | `sensor_msgs/NavSatFix` | Informação de fix do GPS |
| `/time_reference` | `sensor_msgs/TimeReference` | Informação de hora do GPS |
| `/vel` | `geometry_msgs/TwistStamped` | Velocidade do GPS |

As definições das mensagens estão documentadas em:

[sensor_msgs/NavSatFix Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/NavSatFix.html)

[sensor_msgs/TimeReference Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/TimeReference.html)

[geometry_msgs/TwistStamped Documentation (ros.org)](http://docs.ros.org/en/api/geometry_msgs/html/msg/TwistStamped.html)

Pode imprimir estas mensagens de tópico num terminal — o que obtém são os dados GPS. Por exemplo, para imprimir `/fix`:

```
ros2 topic echo /fix
```

O terminal imprime:

![echo fix](../../en/11-ros-read-gps-data/images/3.png)

Aqui, `latitude`, `longitude` e `altitude` são a latitude, a longitude e a altitude.

#### 2. Ler a latitude, a longitude e a altitude

Num terminal:

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

Noutro terminal:

```
ros2 run nmea_navsat_driver read_lat_long.py
```

![read lat long](../../en/11-ros-read-gps-data/images/4.png)

Os dados impressos são a latitude, a longitude e a altitude atuais. Veja o código-fonte, `read_lat_long.py`:

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

O programa subscreve `/fix`, analisa a mensagem na callback e imprime-a no terminal.
