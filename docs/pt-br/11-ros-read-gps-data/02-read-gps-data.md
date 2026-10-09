[English](../../en/11-ros-read-gps-data/02-read-gps-data.md) | [Deutsch](../../de/11-ros-read-gps-data/02-read-gps-data.md) | [Español](../../es/11-ros-read-gps-data/02-read-gps-data.md) | [Français](../../fr/11-ros-read-gps-data/02-read-gps-data.md) | [Italiano](../../it/11-ros-read-gps-data/02-read-gps-data.md) | [日本語](../../ja/11-ros-read-gps-data/02-read-gps-data.md) | [한국어](../../ko/11-ros-read-gps-data/02-read-gps-data.md) | Português (BR) | [Português (PT)](../../pt-pt/11-ros-read-gps-data/02-read-gps-data.md) | [简体中文](../../zh-hans/11-ros-read-gps-data/02-read-gps-data.md) | [繁體中文](../../zh-hant/11-ros-read-gps-data/02-read-gps-data.md)

### Lendo os dados do módulo GPS

**Este recurso lê os dados do GPS a partir de um terminal e os analisa em latitude, longitude e altitude.**

#### 1. Lendo os dados do GPS a partir de um terminal

Em um terminal:

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

![inicialização](../../en/11-ros-read-gps-data/images/1.png)

Agora veja os tópicos:

```
ros2 topic list
```

![lista de tópicos](../../en/11-ros-read-gps-data/images/2.png)

Uma observação sobre os tópicos do GPS:

| Tópico | Tipo | Descrição |
| --- | --- | --- |
| `/extend_fix` | `gps_common/GPSFix` | Mensagem GPSFix contendo o status dos satélites e as informações de fix |
| `/fix` | `sensor_msgs/NavSatFix` | Informações de fix do GPS |
| `/time_reference` | `sensor_msgs/TimeReference` | Informações de hora do GPS |
| `/vel` | `geometry_msgs/TwistStamped` | Velocidade do GPS |

As definições das mensagens estão documentadas em:

[sensor_msgs/NavSatFix Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/NavSatFix.html)

[sensor_msgs/TimeReference Documentation (ros.org)](http://docs.ros.org/en/api/sensor_msgs/html/msg/TimeReference.html)

[geometry_msgs/TwistStamped Documentation (ros.org)](http://docs.ros.org/en/api/geometry_msgs/html/msg/TwistStamped.html)

Você pode imprimir essas mensagens de tópico em um terminal — o que você obtém são os dados do GPS. Por exemplo, para imprimir `/fix`:

```
ros2 topic echo /fix
```

O terminal imprime:

![echo fix](../../en/11-ros-read-gps-data/images/3.png)

Aqui `latitude`, `longitude` e `altitude` são a latitude, a longitude e a altitude.

#### 2. Lendo latitude, longitude e altitude

Em um terminal:

```
ros2 launch nmea_navsat_driver nmea_serial_driver.launch.py
```

Em outro terminal:

```
ros2 run nmea_navsat_driver read_lat_long.py
```

![ler lat long](../../en/11-ros-read-gps-data/images/4.png)

Os dados impressos são a latitude, a longitude e a altitude atuais. Dê uma olhada no código-fonte, `read_lat_long.py`:

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

O programa se inscreve no `/fix`, analisa a mensagem no callback e a imprime no terminal.
