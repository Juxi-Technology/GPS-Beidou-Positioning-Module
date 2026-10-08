#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    rviz_config_dir = os.path.join(
        get_package_share_directory('nmea_navsat_driver'),
        'rviz',
        'gps_path.rviz'
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'port',
            default_value='/dev/ttyUSB0',
            description='Serial port name'
        ),
        DeclareLaunchArgument(
            'baud',
            default_value='9600',
            description='Serial baud rate'
        ),
        DeclareLaunchArgument(
            'frame_id',
            default_value='gps',
            description='Frame ID'
        ),
        DeclareLaunchArgument(
            'time_ref_source',
            default_value='gps',
            description='Time reference source'
        ),
        DeclareLaunchArgument(
            'useRMC',
            default_value='False',
            description='Use RMC sentence'
        ),

        Node(
            package='nmea_navsat_driver',
            executable='nmea_serial_driver.py',
            name='nmea_serial_driver_node',
            output='screen',
            parameters=[{
                'port': LaunchConfiguration('port'),
                'baud': LaunchConfiguration('baud'),
                'frame_id': LaunchConfiguration('frame_id'),
                'time_ref_source': LaunchConfiguration('time_ref_source'),
                'useRMC': LaunchConfiguration('useRMC')
            }]
        ),

        Node(
            package='nmea_navsat_driver',
            executable='gps_path',
            name='gps_path_node',
            output='screen'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_dir]
        )
    ])
