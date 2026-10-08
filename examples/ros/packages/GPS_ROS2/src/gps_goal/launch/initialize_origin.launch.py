from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    lat_arg = DeclareLaunchArgument(
        'latitude',
        default_value='0.0',
        description='Origin latitude (e.g., 31.2304)'
    )

    lon_arg = DeclareLaunchArgument(
        'longitude',
        default_value='0.0',
        description='Origin longitude (e.g., 121.4737)'
    )

    frame_arg = DeclareLaunchArgument(
        'frame_id',
        default_value='map',
        description='Frame ID'
    )

    return LaunchDescription([
        lat_arg,
        lon_arg,
        frame_arg,
    ])
