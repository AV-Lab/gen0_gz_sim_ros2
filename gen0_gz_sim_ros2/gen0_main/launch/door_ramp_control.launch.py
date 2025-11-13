from launch import LaunchDescription
from launch.actions import (
    TimerAction, RegisterEventHandler, DeclareLaunchArgument, GroupAction
)
from launch.conditions import IfCondition, UnlessCondition
from launch.event_handlers import OnProcessStart
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, PythonExpression


def generate_launch_description():
    action_arg = DeclareLaunchArgument('action', default_value='open')
    action_cfg = LaunchConfiguration('action')
    is_close = PythonExpression(['"', action_cfg, '" == "close"'])

    door = Node(
        package='gen0_main',
        executable='door_controller',
        name='door_controller',
        output='screen',
        parameters=[{'action': action_cfg}]
    )

    ramp = Node(
        package='gen0_main',
        executable='ramp_controller',
        name='ramp_controller',
        output='screen',
        parameters=[{'action': action_cfg}]
    )

    # When action != "close": door first, then ramp after 3s
    door_then_ramp = GroupAction(
        actions=[
            door,
            RegisterEventHandler(
                OnProcessStart(
                    target_action=door,
                    on_start=[TimerAction(period=5.0, actions=[ramp])]
                )
            ),
        ],
        condition=UnlessCondition(is_close)
    )

    # When action == "close": ramp first, then door after 3s
    ramp_then_door = GroupAction(
        actions=[
            ramp,
            RegisterEventHandler(
                OnProcessStart(
                    target_action=ramp,
                    on_start=[TimerAction(period=6.0, actions=[door])]
                )
            ),
        ],
        condition=IfCondition(is_close)
    )

    return LaunchDescription([
        action_arg,
        door_then_ramp,
        ramp_then_door,
    ])
