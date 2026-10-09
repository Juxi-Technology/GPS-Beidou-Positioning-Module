[English](../../en/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Deutsch](../../de/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Español](../../es/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | Français | [Italiano](../../it/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [日本語](../../ja/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [한국어](../../ko/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Português (BR)](../../pt-br/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [Português (PT)](../../pt-pt/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [简体中文](../../zh-hans/13-ros-imu-gps-fusion/04-imu-gps-fusion.md) | [繁體中文](../../zh-hant/13-ros-imu-gps-fusion/04-imu-gps-fusion.md)

### Fusion des données IMU et GPS

**Cette fonction fusionne les données IMU et GPS et affiche le résultat dans rviz2.**

#### 1. Exécution

Dans un terminal :

```
ros2 launch imu_gps_localization imu_gps_localization.launch.py 
ros2 bag play gps.bag
```

Au fur et à mesure que le bag est lu, la trajectoire verte dans rviz2 continue de s'étendre — c'est la position fusionnée.


Cet exemple utilise le fichier bag de ce dossier pour la démonstration. En développement réel, vous enregistreriez vous-même les données IMU et GPS avec l'outil `ros2 bag`.

Vous pouvez inspecter le contenu du bag avec **ros2 bag info gps.bag** :


La section `topic` liste ce que le bag a enregistré : les données IMU (`/imu/data` et `/imu/mag`) et GPS (`/nmea_sentence`).

Pendant l'exécution, vous pouvez aussi consulter le graphe des nœuds pour voir comment les topics circulent entre les nœuds :

```
ros2 run rqt_graph rqt_graph
```


#### 2. Le fichier launch

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

Le nœud **imu_gps_localization_node** est celui qui fusionne les données IMU et GPS. Son code source se trouve sous `imu_gps_localization/src` — le fichier clé est **localization_wrapper.cpp**, qui s'abonne aux topics, fusionne les données et publie le résultat. À regarder si cela vous intéresse.
