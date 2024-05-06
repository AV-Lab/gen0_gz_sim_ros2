from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    ld.add_action(DeclareLaunchArgument(
            'actors_scenario',
            description='actors scenario filename'
        ))
    
    ld.add_action(DeclareLaunchArgument(
            'world', 
            description='world filename'
        ))
    
    actors_loader= Node(
            package='gen0_main',
            executable='actors_loader',
            name='actors_loader',
            output='screen',
            parameters=[
                {"actors_scenario": LaunchConfiguration("actors_scenario")},
                {"world": LaunchConfiguration("world")}],
    )

    ld.add_action(actors_loader)


    return ld