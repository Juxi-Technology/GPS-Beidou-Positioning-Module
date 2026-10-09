[English](../../en/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Deutsch](../../de/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Español](../../es/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Français](../../fr/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Italiano](../../it/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [日本語](../../ja/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [한국어](../../ko/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Português (BR)](../../pt-br/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | Português (PT) | [简体中文](../../zh-hans/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [繁體中文](../../zh-hant/13-ros-imu-gps-fusion/04-imu-gps-fusion.md)

### Fusão de Dados de IMU e GPS

**Esta funcionalidade funde os dados de IMU e GPS e apresenta o resultado no rviz2.**

#### 1. Executar

Num terminal:

```
ros2 launch imu_gps_localization imu_gps_localization.launch.py 
ros2 bag play gps.bag
```

À medida que o bag é reproduzido, a trajetória verde no rviz2 continua a estender-se — essa é a posição fundida.


Este exemplo utiliza o ficheiro bag desta pasta para a demonstração. No desenvolvimento real, seria o próprio a gravar os dados de IMU e GPS com a ferramenta `ros2 bag`.

Pode inspecionar o conteúdo do bag com **ros2 bag info gps.bag**:


A secção `topic` lista o que o bag registou: dados de IMU (`/imu/data` e `/imu/mag`) e de GPS (`/nmea_sentence`).

Enquanto está a correr, também pode observar o grafo de nós para ver como os tópicos fluem entre os nós:

```
ros2 run rqt_graph rqt_graph
```


#### 2. O ficheiro launch

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

O nó **imu_gps_localization_node** é o que funde os dados de IMU e GPS. O seu código-fonte está em `imu_gps_localization/src` — o ficheiro principal é **localization_wrapper.cpp**, que subscreve os tópicos, funde os dados e publica o resultado. Vale a pena espreitar, se tiver interesse.
