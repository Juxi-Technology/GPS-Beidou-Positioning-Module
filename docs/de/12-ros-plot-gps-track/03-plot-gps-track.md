[English](../../en/12-ros-plot-gps-track/03-plot-gps-track.md) | Deutsch | [Español](../../es/12-ros-plot-gps-track/03-plot-gps-track.md) | [Français](../../fr/12-ros-plot-gps-track/03-plot-gps-track.md) | [Italiano](../../it/12-ros-plot-gps-track/03-plot-gps-track.md) | [日本語](../../ja/12-ros-plot-gps-track/03-plot-gps-track.md) | [한국어](../../ko/12-ros-plot-gps-track/03-plot-gps-track.md) | [Português (BR)](../../pt-br/12-ros-plot-gps-track/03-plot-gps-track.md) | [Português (PT)](../../pt-pt/12-ros-plot-gps-track/03-plot-gps-track.md) | [简体中文](../../zh-hans/12-ros-plot-gps-track/03-plot-gps-track.md) | [繁體中文](../../zh-hant/12-ros-plot-gps-track/03-plot-gps-track.md)

### Eine GPS-Trajektorie aufzeichnen

**Diese Funktion zeichnet Live-GPS-Daten auf und zeigt sie in rviz2 an.**

#### 1. Funktionsweise

GPS-Daten lassen sich nicht direkt visualisieren, daher transformieren wir das Koordinatensystem: Die Trajektorie wird aus dem WGS-84-Breiten-/Längengrad in ein reales xyz-Koordinatensystem umgerechnet. Mit realen xyz-Koordinaten können wir den Pfad in rviz2 darstellen und die GPS-Trajektorie simulieren. Die Trajektorie wird aufgebaut, indem der Versatz jeder GPS-Koordinate von der ersten Koordinate genommen und aufsummiert wird.

#### 2. Ausführen

In einem Terminal:

```
ros2 launch nmea_navsat_driver gps_path_to_rviz.launch.py
```

![Start](../../en/12-ros-plot-gps-track/images/1.png)

Im Fenster von rviz2 sehen Sie, wie sich die grüne Linie allmählich verlängert, wie unten gezeigt.

![rviz2](../../en/12-ros-plot-gps-track/images/2.png)

#### 3. Die Launch-Datei

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

Drei Nodes werden gestartet: `nmea_serial_driver_node` liest die GPS-Daten, `gps_path_node` zeichnet die GPS-Trajektorie und `rviz2` zeigt sie an.

Der Quellcode von `gps_path_node` ist `gps_path.cpp` unter `nmea_navsat_driver/src` — einen Blick wert.
