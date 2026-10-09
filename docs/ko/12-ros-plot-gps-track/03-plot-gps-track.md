[English](../../en/12-ros-plot-gps-track/03-plot-gps-track.md) | [Deutsch](../../de/12-ros-plot-gps-track/03-plot-gps-track.md) | [Español](../../es/12-ros-plot-gps-track/03-plot-gps-track.md) | [Français](../../fr/12-ros-plot-gps-track/03-plot-gps-track.md) | [Italiano](../../it/12-ros-plot-gps-track/03-plot-gps-track.md) | [日本語](../../ja/12-ros-plot-gps-track/03-plot-gps-track.md) | 한국어 | [Português (BR)](../../pt-br/12-ros-plot-gps-track/03-plot-gps-track.md) | [Português (PT)](../../pt-pt/12-ros-plot-gps-track/03-plot-gps-track.md) | [简体中文](../../zh-hans/12-ros-plot-gps-track/03-plot-gps-track.md) | [繁體中文](../../zh-hant/12-ros-plot-gps-track/03-plot-gps-track.md)

### GPS 궤적 그리기

**이 기능은 실시간 GPS 데이터를 그려 rviz2에 표시합니다.**

#### 1. 동작 원리

GPS 데이터는 그대로는 시각화할 수 없으므로 좌표계를 변환합니다. 궤적을 WGS-84 위도/경도에서 실세계 xyz 좌표계로 변환합니다. 실세계 xyz 좌표가 있으면 rviz2에서 경로를 표시하고 GPS 궤적을 시뮬레이션할 수 있습니다. 궤적은 각 GPS 좌표의 첫 번째 좌표로부터의 오프셋을 취하여 합산함으로써 누적됩니다.

#### 2. 실행

터미널에서:

```
ros2 launch nmea_navsat_driver gps_path_to_rviz.launch.py
```

![실행](../../en/12-ros-plot-gps-track/images/1.png)

rviz2 창에서 아래와 같이 녹색 선이 점차 길어지는 것을 볼 수 있습니다.

![rviz2](../../en/12-ros-plot-gps-track/images/2.png)

#### 3. launch 파일

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

세 개의 노드가 시작됩니다. `nmea_serial_driver_node`는 GPS 데이터를 읽고, `gps_path_node`는 GPS 궤적을 그리며, `rviz2`는 이를 표시합니다.

`gps_path_node`의 소스는 `nmea_navsat_driver/src` 아래의 `gps_path.cpp`이며, 한번 살펴볼 만합니다.
