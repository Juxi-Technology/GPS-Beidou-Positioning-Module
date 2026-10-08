from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    frame_id_arg = DeclareLaunchArgument(
        'frame_id',
        default_value='map',
        description='Frame ID for the goal pose'
    )

    dry_run_arg = DeclareLaunchArgument(
        'dry_run',
        default_value='True',
        description='Dry run mode: only print conversion result, not send to Nav2'
    )

    gps_goal_node = Node(
        package='gps_goal',
        executable='gps_goal_node.py',
        name='gps_goal',
        output='screen',
        parameters=[{
            'frame_id': LaunchConfiguration('frame_id'),
            'dry_run': LaunchConfiguration('dry_run'),
        }]
    )

    return LaunchDescription([
        frame_id_arg,
        dry_run_arg,
        gps_goal_node,
    ])
