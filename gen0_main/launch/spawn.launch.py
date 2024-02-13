from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument, LogInfo, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command, TextSubstitution, PythonExpression
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os

def generate_launch_description():
    world_arg=DeclareLaunchArgument(
            'world',
            default_value='san_roundabout',
            description='Name of the world file (without extension) to be used in Gazebo simulation'
    )
    sim_arg=DeclareLaunchArgument(
            'use_sim_time', 
            default_value='false', 
            choices=['true', 'false']
    )
    pkg_share_dir = get_package_share_directory('gen0_main')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    bridge_file= PathJoinSubstitution([pkg_share_dir, 'config', 'bridge.yaml'])
    world_file= PathJoinSubstitution([pkg_share_dir, 'worlds/', LaunchConfiguration('world'), PythonExpression(["'", LaunchConfiguration('world'), "'", ' + ".sdf"'])])
    vehicle_file=os.path.join(pkg_share_dir, 'urdf', 'gen0_model.sdf')

    os.environ['IGN_GAZEBO_RESOURCE_PATH']= pkg_share_dir + "/meshes"

    with open(vehicle_file, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        world_arg,
        sim_arg,
        IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args':
            world_file
        }.items(),
        ),
        Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': bridge_file,
            'qos_overrides./tf_static.publisher.durability': 'transient_local',
        }],
        output='screen'
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='both',
            parameters=[
                {'use_sim_time': LaunchConfiguration('use_sim_time')},
                {'robot_description': robot_desc},
            ]
        ),
        # Node(
        #     package='rviz2',
        #     executable='rviz2',
        #     arguments=['-d', os.path.join(pkg_share_dir, 'config', 'gen0_main.rviz')],
        #     # condition=IfCondition(LaunchConfiguration('rviz'))
        # ),
        Node(
            package='gen0_main',
            executable='ground_truth_publisher',
        ),
    ])




