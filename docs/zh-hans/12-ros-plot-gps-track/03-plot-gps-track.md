[English](../../en/12-ros-plot-gps-track/03-plot-gps-track.md) | [Deutsch](../../de/12-ros-plot-gps-track/03-plot-gps-track.md) | [Español](../../es/12-ros-plot-gps-track/03-plot-gps-track.md) | [Français](../../fr/12-ros-plot-gps-track/03-plot-gps-track.md) | [Italiano](../../it/12-ros-plot-gps-track/03-plot-gps-track.md) | [日本語](../../ja/12-ros-plot-gps-track/03-plot-gps-track.md) | [한국어](../../ko/12-ros-plot-gps-track/03-plot-gps-track.md) | [Português (BR)](../../pt-br/12-ros-plot-gps-track/03-plot-gps-track.md) | [Português (PT)](../../pt-pt/12-ros-plot-gps-track/03-plot-gps-track.md) | 简体中文 | [繁體中文](../../zh-hant/12-ros-plot-gps-track/03-plot-gps-track.md)

### 绘制GPS轨迹

**该功能绘制实时GPS数据信息，并且在rviz2中展示出来。**

#### 1、实现原理

GPS的信息直接可视化是不可能，我们需要转换下坐标系，将GPS轨迹，从经纬度WGS-84坐标转换到真实世界xyz坐标系下。有了在真实世界的xyz坐标，我们就可以通过rviz2去显示路径，模拟出是GPS的轨迹。轨迹就是累计每个gps坐标相对与第一个坐标的位置，然后累加即可得到轨迹。

#### 2、启动步骤

终端输入，

```
ros2 launch nmea_navsat_driver gps_path_to_rviz.launch.py
```

![img_20260611114846](../../en/12-ros-plot-gps-track/images/1.png)

在rviz2显示的界面，我们可以看到，绿色的线在不断慢慢地延伸，如下图所示，

![img_20260611114958](../../en/12-ros-plot-gps-track/images/2.png)

#### 3、launch代码解析

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

启动了三个节点，分别是nmea_serial_driver_node读取GPS数据、gps_path_node绘制GPS数据轨迹和rviz2节点。

其中，gps_path_node这个节点的源码gps_path.cpp在nmea_navsat_driver/src下，可以去看看。
