from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    config_dir = os.path.join(
        get_package_share_directory('gen0_main'),
        'config',
        'nav2_params.yaml'
    )
    
    print(f"Loading parameters from: {config_dir}")
    
    return LaunchDescription([
        Node(
            package='nav2_costmap_2d',
            executable='nav2_costmap_2d',
            name='local_costmap',
            output='screen',
            parameters=[config_dir]
        ),
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_costmap',
            output='screen',
            parameters=[{
                'autostart': True,
                'node_names': ['costmap/costmap']
            }]
        )
    ])
