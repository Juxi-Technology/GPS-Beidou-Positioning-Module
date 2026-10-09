[English](../../en/12-ros-plot-gps-track/03-plot-gps-track.md) | [Deutsch](../../de/12-ros-plot-gps-track/03-plot-gps-track.md) | [Español](../../es/12-ros-plot-gps-track/03-plot-gps-track.md) | Français | [Italiano](../../it/12-ros-plot-gps-track/03-plot-gps-track.md) | [日本語](../../ja/12-ros-plot-gps-track/03-plot-gps-track.md) | [한국어](../../ko/12-ros-plot-gps-track/03-plot-gps-track.md) | [Português (BR)](../../pt-br/12-ros-plot-gps-track/03-plot-gps-track.md) | [Português (PT)](../../pt-pt/12-ros-plot-gps-track/03-plot-gps-track.md) | [简体中文](../../zh-hans/12-ros-plot-gps-track/03-plot-gps-track.md) | [繁體中文](../../zh-hant/12-ros-plot-gps-track/03-plot-gps-track.md)

### Tracé d'une trajectoire GPS

**Cette fonction trace les données GPS en direct et les affiche dans rviz2.**

#### 1. Fonctionnement

Les données GPS ne peuvent pas être visualisées directement ; nous transformons donc le système de coordonnées : la trajectoire est convertie de la latitude/longitude WGS-84 en un repère xyz réel. Avec des coordonnées xyz réelles, nous pouvons afficher le trajet dans rviz2 et simuler la trajectoire GPS. La trajectoire est accumulée en prenant l'écart de chaque coordonnée GPS par rapport à la première coordonnée et en les additionnant.

#### 2. Exécution

Dans un terminal :

```
ros2 launch nmea_navsat_driver gps_path_to_rviz.launch.py
```

![lancement](../../en/12-ros-plot-gps-track/images/1.png)

Dans la fenêtre rviz2, vous pouvez voir la ligne verte s'étendre progressivement, comme ci-dessous.

![rviz2](../../en/12-ros-plot-gps-track/images/2.png)

#### 3. Le fichier launch

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

Trois nœuds sont démarrés : `nmea_serial_driver_node` lit les données GPS, `gps_path_node` trace la trajectoire GPS, et `rviz2` l'affiche.

Le code source de `gps_path_node` est `gps_path.cpp`, sous `nmea_navsat_driver/src` — à regarder.
