import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    share = get_package_share_directory('lab_py')
    return LaunchDescription([
        DeclareLaunchArgument('rviz', default_value='true'),
        Node(package='lab_py', executable='sensor', output='screen'),
        Node(package='lab_cpp', executable='monitor', output='screen'),
        Node(package='lab_py', executable='rover', output='screen'),
        Node(package='lab_py', executable='guard', output='screen'),
        Node(package='lab_py', executable='patrol', output='screen',
             parameters=[os.path.join(share, 'config', 'patrol.yaml')]),
        Node(package='rviz2', executable='rviz2', output='screen',
             condition=IfCondition(LaunchConfiguration('rviz')),
             arguments=['-d', os.path.join(share, 'config', 'course.rviz')]),
    ])
