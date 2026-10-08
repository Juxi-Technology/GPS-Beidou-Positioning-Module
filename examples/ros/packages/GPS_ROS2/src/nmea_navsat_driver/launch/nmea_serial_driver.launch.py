#!/usr/bin/env python3
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
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
        )
    ])
