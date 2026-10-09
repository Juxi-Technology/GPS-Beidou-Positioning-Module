[English](../../en/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Deutsch](../../de/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Español](../../es/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Français](../../fr/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Italiano](../../it/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [日本語](../../ja/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [한국어](../../ko/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Português (BR)](../../pt-br/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Português (PT)](../../pt-pt/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | 简体中文 | [繁體中文](../../zh-hant/13-ros-imu-gps-fusion/04-imu-gps-fusion.md)

### 融合IMU和GPS数据

**该功能融合IMU和GPS数据，并且在rviz2中展示融合后的数据。**

#### 1 、运行

终端输入

```
ros2 launch imu_gps_localization imu_gps_localization.launch.py 
ros2 bag play gps.bag
```

运行后，随着数据包的播放，在rviz2中，绿色的轨迹也是不断地延伸，代表着的是融合后的位置，


在本案例中，我们使用文件夹中的数据包来做个演示，实际开发中，需要自己使用ros2 bag工具记录IMU和GPS的数据。

我们可以通过**ros2 bag info gps.bag**来查看这个数据包的内容，


topic那部分的内容就是这个数据包所记录的话题，可以看出包含了IMU（/imu/data和 /imu/mag和GPS（/nmea_sentence）数据。

在运行过程中，我们也可以查看节点图，看看节点之间的话题传输情况，终端输入

```
ros2 run rqt_graph rqt_graph
```


#### 2、launch文件

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    acc_noise_arg = DeclareLaunchArgument('acc_noise', default_value='1e-2')
    gyro_noise_arg = DeclareLaunchArgument('gyro_noise', default_value='1e-4')
    acc_bias_noise_arg = DeclareLaunchArgument('acc_bias_noise', default_value='1e-6')
    gyro_bias_noise_arg = DeclareLaunchArgument('gyro_bias_noise', default_value='1e-8')

    I_p_Gps_x_arg = DeclareLaunchArgument('I_p_Gps_x', default_value='0.0')
    I_p_Gps_y_arg = DeclareLaunchArgument('I_p_Gps_y', default_value='0.0')
    I_p_Gps_z_arg = DeclareLaunchArgument('I_p_Gps_z', default_value='0.0')

    log_folder_arg = DeclareLaunchArgument('log_folder', 
        default_value=get_package_share_directory('imu_gps_localization'))

    acc_noise = LaunchConfiguration('acc_noise')
    gyro_noise = LaunchConfiguration('gyro_noise')
    acc_bias_noise = LaunchConfiguration('acc_bias_noise')
    gyro_bias_noise = LaunchConfiguration('gyro_bias_noise')

    I_p_Gps_x = LaunchConfiguration('I_p_Gps_x')
    I_p_Gps_y = LaunchConfiguration('I_p_Gps_y')
    I_p_Gps_z = LaunchConfiguration('I_p_Gps_z')

    log_folder = LaunchConfiguration('log_folder')

    nmea_topic_driver_node = Node(
        package='nmea_navsat_driver',
        executable='nmea_topic_driver',
        name='nmea_topic_driver',
        output='screen'
    )

    imu_gps_localization_node = Node(
        package='imu_gps_localization',
        executable='imu_gps_localization_node',
        name='imu_gps_localization_node',
        output='screen',
        parameters=[{
            'acc_noise': acc_noise,
            'gyro_noise': gyro_noise,
            'acc_bias_noise': acc_bias_noise,
            'gyro_bias_noise': gyro_bias_noise,
            'I_p_Gps_x': I_p_Gps_x,
            'I_p_Gps_y': I_p_Gps_y,
            'I_p_Gps_z': I_p_Gps_z,
            'log_folder': log_folder
        }]
    )

    rviz_config = os.path.join(
        get_package_share_directory('imu_gps_localization'),
        'rviz',
        'default.rviz'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config]
    )

    return LaunchDescription([
        acc_noise_arg,
        gyro_noise_arg,
        acc_bias_noise_arg,
        gyro_bias_noise_arg,
        I_p_Gps_x_arg,
        I_p_Gps_y_arg,
        I_p_Gps_z_arg,
        log_folder_arg,
        nmea_topic_driver_node,
        imu_gps_localization_node,
        rviz_node
    ])
```

其中，**imu_gps_localization_node**这个节点就做融合IMU和GPS数据的，其源码位置在imu_gps_localization/src，重点是看**localization_wrapper.cpp**，里边包括了订阅话题，融合数据以及发布话题数据，感兴趣的可以去看看。
