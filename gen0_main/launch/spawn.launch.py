from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument, LogInfo, IncludeLaunchDescription, ExecuteProcess, OpaqueFunction 
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command, TextSubstitution, PythonExpression
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os


def actors_launch(context, *args, **kwargs):
    actors_scenario = LaunchConfiguration('actors_scenario').perform(context)
    world = LaunchConfiguration('world').perform(context)

    pkg_share_dir = get_package_share_directory('gen0_main')
    scenario_file_path = os.path.join(pkg_share_dir, 'worlds', 'scenarios', world, f"{actors_scenario}.sdf")

    actions = []

    actors_launch_file = os.path.join(pkg_share_dir, 'launch', 'actors.launch.py')
    # If the file exists, include the actors.launch.py and add it to the actions list
    actions.append(IncludeLaunchDescription(
        PythonLaunchDescriptionSource(actors_launch_file),
        launch_arguments={
            'world': world,
            'actors_scenario': actors_scenario
        }.items(),
    ))

    if not os.path.exists(scenario_file_path):
        actions.append(LogInfo(msg=f"\033[93m[WARNING] Scenario {actors_scenario} does not exist for world {world}\033[0m"))
        
    return actions


def generate_launch_description():
    # Launch Arugments
    world_arg=DeclareLaunchArgument(
            'world',
            default_value='san_roundabout',
            description='Name of the world file (without extension) to be used in Gazebo simulation'
    )
    sim_arg=DeclareLaunchArgument(
            'use_sim_time', 
            default_value='true', 
            choices=['true', 'false']
    )
    actors_arg=DeclareLaunchArgument(
            'actors_scenario', 
            default_value= "", 
            description='The scenario for pedestrians (without extension to be used in Gazebo world file)'
    )
    rviz_arg=DeclareLaunchArgument(
            'rviz', 
            default_value= "false", 
            choices=['true', 'false']
    )
    autoware_arg=DeclareLaunchArgument(
            'autoware', 
            default_value= "false", 
            choices=['true', 'false']
    )

    # Paths
    pkg_share_dir = get_package_share_directory('gen0_main')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    bridge_file= PathJoinSubstitution([pkg_share_dir, 'config', 'bridge.yaml'])
    world_file= PathJoinSubstitution([pkg_share_dir, 'worlds/', LaunchConfiguration('world'), PythonExpression(["'", LaunchConfiguration('world'), "'", ' + ".sdf"'])])
    vehicle_file=os.path.join(pkg_share_dir, 'urdf', 'gen0_model.sdf')
    os.environ['IGN_GAZEBO_RESOURCE_PATH']= pkg_share_dir + "/meshes" # Load the meshes to the gazebo server

    # Files
    with open(vehicle_file, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        world_arg,
        sim_arg,
        actors_arg,
        rviz_arg,
        autoware_arg,
        OpaqueFunction(function=actors_launch),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
            ),
            launch_arguments={
                    'gz_args': world_file
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
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', os.path.join(pkg_share_dir, 'config', 'gen0_main.rviz')],
            condition=IfCondition(LaunchConfiguration('rviz'))
        ),
        Node(
            package='gen0_main',
            executable='ground_truth_publisher',
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
            condition=UnlessCondition(LaunchConfiguration('autoware'))
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='world_map_tf',
            namespace='',
            arguments=['-20.6991', '-22.4324', '0.0', '1.0302', '0.0', '0.0', 'world', 'map'],
            parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        )
    ])




