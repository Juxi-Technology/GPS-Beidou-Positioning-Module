[English](../../en/12-ros-plot-gps-track/03-plot-gps-track.md) | [Deutsch](../../de/12-ros-plot-gps-track/03-plot-gps-track.md) | [Español](../../es/12-ros-plot-gps-track/03-plot-gps-track.md) | [Français](../../fr/12-ros-plot-gps-track/03-plot-gps-track.md) | [Italiano](../../it/12-ros-plot-gps-track/03-plot-gps-track.md) | [日本語](../../ja/12-ros-plot-gps-track/03-plot-gps-track.md) | [한국어](../../ko/12-ros-plot-gps-track/03-plot-gps-track.md) | [Português (BR)](../../pt-br/12-ros-plot-gps-track/03-plot-gps-track.md) | Português (PT) | [简体中文](../../zh-hans/12-ros-plot-gps-track/03-plot-gps-track.md) | [繁體中文](../../zh-hant/12-ros-plot-gps-track/03-plot-gps-track.md)

### Traçar uma Trajetória GPS

**Esta funcionalidade traça os dados GPS em tempo real e apresenta-os no rviz2.**

#### 1. Como funciona

Os dados GPS não podem ser visualizados diretamente, por isso transformamos o sistema de coordenadas: a trajetória é convertida de latitude/longitude WGS-84 para um referencial xyz do mundo real. Com coordenadas xyz do mundo real, podemos apresentar o percurso no rviz2 e simular a trajetória GPS. A trajetória é acumulada tomando o desvio de cada coordenada GPS em relação à primeira coordenada e somando-os.

#### 2. Executar

Num terminal:

```
ros2 launch nmea_navsat_driver gps_path_to_rviz.launch.py
```

![arranque](../../en/12-ros-plot-gps-track/images/1.png)

Na janela do rviz2, pode ver a linha verde a estender-se gradualmente, como mostrado abaixo.

![rviz2](../../en/12-ros-plot-gps-track/images/2.png)

#### 3. O ficheiro launch

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    port_arg = DeclareLaunchArgument('port', default_value='/dev/myserial')
    baud_arg = DeclareLaunchArgument('baud', default_value='9600')
    frame_id_arg = DeclareLaunchArgument('frame_id', default_value='gps')
    time_ref_source_arg = DeclareLaunchArgument('time_ref_source', default_value='gps')
    useRMC_arg = DeclareLaunchArgument('useRMC', default_value='False')

    port = LaunchConfiguration('port')
    baud = LaunchConfiguration('baud')
    frame_id = LaunchConfiguration('frame_id')
    time_ref_source = LaunchConfiguration('time_ref_source')
    useRMC = LaunchConfiguration('useRMC')

    nmea_serial_driver_node = Node(
        package='nmea_navsat_driver',
        executable='nmea_serial_driver',
        name='nmea_serial_driver_node',
        output='screen',
        parameters=[{
            'port': port,
            'baud': baud,
            'frame_id': frame_id,
            'time_ref_source': time_ref_source,
            'useRMC': useRMC
        }]
    )

    gps_path_node = Node(
        package='nmea_navsat_driver',
        executable='Draw_GPS_Path',
        name='gps_path_node',
        output='screen'
    )

    rviz_config = os.path.join(
        get_package_share_directory('nmea_navsat_driver'),
        'rviz',
        'gps_path.rviz'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config]
    )

    return LaunchDescription([
        port_arg,
        baud_arg,
        frame_id_arg,
        time_ref_source_arg,
        useRMC_arg,
        nmea_serial_driver_node,
        gps_path_node,
        rviz_node
    ])
```

São iniciados três nós: `nmea_serial_driver_node` lê os dados GPS, `gps_path_node` desenha a trajetória GPS e `rviz2` apresenta-a.

O código-fonte de `gps_path_node` é `gps_path.cpp`, em `nmea_navsat_driver/src` — vale a pena espreitar.
