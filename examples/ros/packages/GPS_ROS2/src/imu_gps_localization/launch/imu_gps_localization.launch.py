import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    acc_noise = LaunchConfiguration('acc_noise', default='1e-2')
    gyro_noise = LaunchConfiguration('gyro_noise', default='1e-4')
    acc_bias_noise = LaunchConfiguration('acc_bias_noise', default='1e-6')
    gyro_bias_noise = LaunchConfiguration('gyro_bias_noise', default='1e-8')
    I_p_Gps_x = LaunchConfiguration('I_p_Gps_x', default='0.0')
    I_p_Gps_y = LaunchConfiguration('I_p_Gps_y', default='0.0')
    I_p_Gps_z = LaunchConfiguration('I_p_Gps_z', default='0.0')
    log_folder = LaunchConfiguration('log_folder', default='/tmp')

    declare_acc_noise_cmd = DeclareLaunchArgument(
        'acc_noise',
        default_value='1e-2',
        description='Accelerometer noise')

    declare_gyro_noise_cmd = DeclareLaunchArgument(
        'gyro_noise',
        default_value='1e-4',
        description='Gyroscope noise')

    declare_acc_bias_noise_cmd = DeclareLaunchArgument(
        'acc_bias_noise',
        default_value='1e-6',
        description='Accelerometer bias noise')

    declare_gyro_bias_noise_cmd = DeclareLaunchArgument(
        'gyro_bias_noise',
        default_value='1e-8',
        description='Gyroscope bias noise')

    declare_I_p_Gps_x_cmd = DeclareLaunchArgument(
        'I_p_Gps_x',
        default_value='0.0',
        description='GPS position x in IMU frame')

    declare_I_p_Gps_y_cmd = DeclareLaunchArgument(
        'I_p_Gps_y',
        default_value='0.0',
        description='GPS position y in IMU frame')

    declare_I_p_Gps_z_cmd = DeclareLaunchArgument(
        'I_p_Gps_z',
        default_value='0.0',
        description='GPS position z in IMU frame')

    declare_log_folder_cmd = DeclareLaunchArgument(
        'log_folder',
        default_value='/tmp',
        description='Log folder path')

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
        declare_acc_noise_cmd,
        declare_gyro_noise_cmd,
        declare_acc_bias_noise_cmd,
        declare_gyro_bias_noise_cmd,
        declare_I_p_Gps_x_cmd,
        declare_I_p_Gps_y_cmd,
        declare_I_p_Gps_z_cmd,
        declare_log_folder_cmd,
        imu_gps_localization_node,
        rviz_node
    ])
