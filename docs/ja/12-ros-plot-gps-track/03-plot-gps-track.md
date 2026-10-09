[English](../../en/12-ros-plot-gps-track/03-plot-gps-track.md) | [Deutsch](../../de/12-ros-plot-gps-track/03-plot-gps-track.md) | [Español](../../es/12-ros-plot-gps-track/03-plot-gps-track.md) | [Français](../../fr/12-ros-plot-gps-track/03-plot-gps-track.md) | [Italiano](../../it/12-ros-plot-gps-track/03-plot-gps-track.md) | 日本語 | [한국어](../../ko/12-ros-plot-gps-track/03-plot-gps-track.md) | [Português (BR)](../../pt-br/12-ros-plot-gps-track/03-plot-gps-track.md) | [Português (PT)](../../pt-pt/12-ros-plot-gps-track/03-plot-gps-track.md) | [简体中文](../../zh-hans/12-ros-plot-gps-track/03-plot-gps-track.md) | [繁體中文](../../zh-hant/12-ros-plot-gps-track/03-plot-gps-track.md)

### GPS 軌跡の描画

**この機能は、ライブの GPS データを描画し、rviz2 に表示します。**

#### 1. 仕組み

GPS データはそのままでは可視化できないため、座標系を変換します。軌跡を WGS-84 の緯度・経度から実世界の xyz 座標系に変換します。実世界の xyz 座標があれば、rviz2 上で経路を表示し、GPS 軌跡をシミュレートできます。軌跡は、各 GPS 座標の最初の座標からのオフセットを取り、それらを合計することで蓄積されます。

#### 2. 実行方法

ターミナルで：

```
ros2 launch nmea_navsat_driver gps_path_to_rviz.launch.py
```

![launch](../../en/12-ros-plot-gps-track/images/1.png)

rviz2 のウィンドウで、以下に示すように緑色の線が徐々に伸びていくのが確認できます。

![rviz2](../../en/12-ros-plot-gps-track/images/2.png)

#### 3. launch ファイル

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

3 つのノードが起動します。`nmea_serial_driver_node` が GPS データを読み取り、`gps_path_node` が GPS 軌跡を描画し、`rviz2` がそれを表示します。

`gps_path_node` のソースは `nmea_navsat_driver/src` 配下の `gps_path.cpp` です。一見の価値があります。
