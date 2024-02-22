from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
from launch.actions import LogInfo 


def generate_launch_description():

    return LaunchDescription([
        DeclareLaunchArgument(
            'actors_scenario',
            description='actors scenario filename'
        ),
        DeclareLaunchArgument(
            'world', 
            description='world filename'
        ),
        Node(
            package='gen0_main',
            executable='actors_loader',
            name='actors_loader',
            output='screen',
            parameters=[
                {"actors_scenario": LaunchConfiguration("actors_scenario")},
                {"world": LaunchConfiguration("world")}],
        ),
    ])
