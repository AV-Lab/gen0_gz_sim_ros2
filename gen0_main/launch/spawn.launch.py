from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument, LogInfo, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
import os

def generate_launch_description():
    pkg_share_dir = get_package_share_directory('gen0_main')
    # xacro_file = PathJoinSubstitution([pkg_share_dir, 'urdf', 'description.urdf.xacro'])
    bridge_file= PathJoinSubstitution([pkg_share_dir, 'config', 'bridge.yaml'])
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    world_file= PathJoinSubstitution([pkg_share_dir, 'worlds/san_roundabout', 'san_roundabout.sdf'])
    # ros_ign_gazebo = get_package_share_directory('ros_ign_gazebo')
    # ign_gazebo_launch = PathJoinSubstitution([ros_ign_gazebo, 'launch', 'ign_gazebo.launch.py'])

    sdf_file=os.path.join(pkg_share_dir, 'urdf', 'gen0_model.sdf')

    os.environ['IGN_GAZEBO_RESOURCE_PATH']= pkg_share_dir + "/meshes"

    with open(sdf_file, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        # DeclareLaunchArgument('namespace', default_value='gen0_model'),
        DeclareLaunchArgument('use_sim_time', default_value='false', choices=['true', 'false']),
        IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args':
            world_file
        }.items(),
        ),
        # Node(
        #     package='joint_state_publisher',
        #     executable='joint_state_publisher',
        #     name='joint_state_publisher',
        #     output='screen',
        #     parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        #     remappings=[
        #         ('/tf', 'tf'),
        #         ('/tf_static', 'tf_static')
        #     ]
        # ),
        # IncludeLaunchDescription(
        # PythonLaunchDescriptionSource([ign_gazebo_launch]),
        # launch_arguments=[
        #     ('ign_args', [world_file])
        # ]
        # ),
        # Node(
        #     package='ros_ign_gazebo',
        #     executable='create',
        #     arguments=['-x', '-25.00',
        #                '-y', '13.5288',
        #                '-z', '0.1',
        #                '-Y', '1.0',
        #                 # '-x', '0.0',
        #                 # '-y', '0.0',
        #                 # '-z', '0.0',
        #                 # '-Y', '0.0',
        #                '-topic', 'robot_description'],
        #     output='screen'
        # ),
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
        # Node(
        #     package='gen0_main',
        #     executable='odom_frame_corrector',
        # ),
    ])




