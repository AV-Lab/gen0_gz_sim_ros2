#!/bin/bash

# Update the workspace path variable
WORKSPACE=~/gen0_gz_sim_ros2

cd "$WORKSPACE"


mkdir -p "$WORKSPACE/src/gen0_gz_sim_ros2/gen0_gz_sim_ros2/gz_plugins/build"
cd "$WORKSPACE/src/gen0_gz_sim_ros2/gen0_gz_sim_ros2/gz_plugins/build" || exit
cmake ..
make
cd ..
export GZ_SIM_SYSTEM_PLUGIN_PATH=$(pwd)/build

cd "$WORKSPACE" || exit
source /opt/ros/jazzy/setup.bash
colcon build --packages-ignore race_plan_control
source install/setup.bash

ros2 launch gen0_main spawn.launch.py world:=san_full actors_scenario:=walking_actors ground_truth_localization:=true use_gui_config:=true

# rviz:=true
