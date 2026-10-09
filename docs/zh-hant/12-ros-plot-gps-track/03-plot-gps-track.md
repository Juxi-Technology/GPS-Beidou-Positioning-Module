[English](../../en/12-ros-plot-gps-track/03-plot-gps-track.md) | [Deutsch](../../de/12-ros-plot-gps-track/03-plot-gps-track.md) | [Español](../../es/12-ros-plot-gps-track/03-plot-gps-track.md) | [Français](../../fr/12-ros-plot-gps-track/03-plot-gps-track.md) | [Italiano](../../it/12-ros-plot-gps-track/03-plot-gps-track.md) | [日本語](../../ja/12-ros-plot-gps-track/03-plot-gps-track.md) | [한국어](../../ko/12-ros-plot-gps-track/03-plot-gps-track.md) | [Português (BR)](../../pt-br/12-ros-plot-gps-track/03-plot-gps-track.md) | [Português (PT)](../../pt-pt/12-ros-plot-gps-track/03-plot-gps-track.md) | [简体中文](../../zh-hans/12-ros-plot-gps-track/03-plot-gps-track.md) | 繁體中文

### 繪製GPS軌跡

**該功能繪製即時GPS資料資訊，並且在rviz2中展示出來。**

#### 1、實現原理

GPS的資訊直接視覺化是不可能，我們需要轉換下座標系，將GPS軌跡，從經緯度WGS-84座標轉換到真實世界xyz座標系下。有了在真實世界的xyz座標，我們就可以透過rviz2去顯示路徑，模擬出是GPS的軌跡。軌跡就是累計每個gps座標相對與第一個座標的位置，然後累加即可得到軌跡。

#### 2、啟動步驟

終端機輸入，

```
ros2 launch nmea_navsat_driver gps_path_to_rviz.launch.py
```

![img_20260611114846](../../en/12-ros-plot-gps-track/images/1.png)

在rviz2顯示的介面，我們可以看到，綠色的線在不斷慢慢地延伸，如下圖所示，

![img_20260611114958](../../en/12-ros-plot-gps-track/images/2.png)

#### 3、launch程式碼解析

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

啟動了三個節點，分別是nmea_serial_driver_node讀取GPS資料、gps_path_node繪製GPS資料軌跡和rviz2節點。

其中，gps_path_node這個節點的原始碼gps_path.cpp在nmea_navsat_driver/src下，可以去看看。
