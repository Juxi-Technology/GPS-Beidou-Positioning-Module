from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.conditions import IfCondition


def generate_launch_description():
    use_fake_server_arg = DeclareLaunchArgument(
        'use_fake_server',
        default_value='True',
        description='Use fake Nav2 server for demo/testing'
    )

    frame_id_arg = DeclareLaunchArgument(
        'frame_id',
        default_value='map',
        description='Frame ID for the goal pose'
    )

    fake_nav2_server = Node(
        package='gps_goal',
        executable='fake_nav2_server.py',
        name='fake_nav2_server',
        output='screen',
        condition=IfCondition(LaunchConfiguration('use_fake_server'))
    )

    gps_goal_node = Node(
        package='gps_goal',
        executable='gps_goal_node.py',
        name='gps_goal',
        output='screen',
        parameters=[{
            'frame_id': LaunchConfiguration('frame_id'),
            'dry_run': False,
        }]
    )

    return LaunchDescription([
        use_fake_server_arg,
        frame_id_arg,
        fake_nav2_server,
        gps_goal_node,
    ])
