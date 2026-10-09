[English](../../en/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Deutsch](../../de/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Español](../../es/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Français](../../fr/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Italiano](../../it/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [日本語](../../ja/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | 한국어 | [Português (BR)](../../pt-br/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Português (PT)](../../pt-pt/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [简体中文](../../zh-hans/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [繁體中文](../../zh-hant/13-ros-imu-gps-fusion/04-imu-gps-fusion.md)

### IMU와 GPS 데이터 융합

**이 기능은 IMU와 GPS 데이터를 융합하여 그 결과를 rviz2에 표시합니다.**

#### 1. 실행

터미널에서:

```
ros2 launch imu_gps_localization imu_gps_localization.launch.py 
ros2 bag play gps.bag
```

bag이 재생되면서 rviz2의 녹색 궤적이 계속 길어지며, 이것이 융합된 위치입니다.


이 예제는 이 폴더의 bag 파일을 데모용으로 사용합니다. 실제 개발에서는 `ros2 bag` 도구로 IMU와 GPS 데이터를 직접 기록하게 됩니다.

**ros2 bag info gps.bag**로 bag의 내용을 확인할 수 있습니다:


`topic` 섹션에는 bag이 기록한 내용, 즉 IMU(`/imu/data`, `/imu/mag`)와 GPS(`/nmea_sentence`) 데이터가 나열됩니다.

실행 중에는 노드 그래프를 보고 노드 간에 토픽이 어떻게 흐르는지 확인할 수도 있습니다:

```
ros2 run rqt_graph rqt_graph
```


#### 2. launch 파일

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

**imu_gps_localization_node** 노드가 IMU와 GPS 데이터를 융합하는 노드입니다. 소스는 `imu_gps_localization/src` 아래에 있으며, 핵심 파일은 **localization_wrapper.cpp**로, 토픽을 구독하고 데이터를 융합하여 결과를 발행합니다. 관심이 있다면 살펴볼 만합니다.
