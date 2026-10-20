import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory('lab_py')
    world = os.path.join(share, 'worlds', 'rover.sdf')
    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true'),
        ExecuteProcess(cmd=['gz', 'sim', '-r', '-s', world], output='screen'),
        ExecuteProcess(cmd=['gz', 'sim', '-g'], output='screen',
                       condition=IfCondition(LaunchConfiguration('gui'))),
        Node(package='ros_gz_bridge', executable='parameter_bridge', output='screen',
             parameters=[{'config_file': os.path.join(share, 'config', 'bridge.yaml')}]),
    ])
