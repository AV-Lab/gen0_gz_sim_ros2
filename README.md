# gen0_gz_sim_ros2
gen0_gz_sim is an under development simulation ennvironemnt of an autonomous shuttle (gen0) based on ROS2 and gazebo ignition, it currently includes path following controllers which navigates the vehicle based on a predefined global path and ground truth localization with ackermann kinematics.

![](/assets/images/simulation.png)

## Table of Contents 
- [System Requirements](#system-requirements)
- [Dependencies](#dependencies)
- [Source Installation](#source-installation)
- [Docker Installation](#docker-installation)
- [Quick Start Guide](#quick-start-guide)
- [Development Guide](#development-guide)
- [Known issues](#known-issues)


## System Rquirements 
The system requirements depend on the world and number of pedestrians present during the runtime, furthermore, the following specifications were used to develop the simulation environement:
- Ubuntu 22.04 LTS
- RAM 64GB 
- RTX 2080ti
- i9 9900k
  
## Dependencies
-  ROS2 Humble: https://docs.ros.org/en/humble/Installation.html
-  colcon to build packages
```
sudo apt install python3-colcon-common-extensions
```
-  Gazebo ignition 6.x (Fortress for ROS2 Humble): https://gazebosim.org/docs/fortress/install_ubuntu
- ros_gz package
```
sudo apt-get install ros-humble-ros-gz
```
-  transforms3d
```
pip install transforms3d
```
- ros-humble-tf-transformations
```
sudo apt install ros-humble-tf-transformations
```

## Source Installation
1) Create a ROS2 workspace
```
mkdir ~/gen0_gz_sim_ros2
cd ~/gen0_gz_sim_ros2
mkdir src
cd src
```
2) Clone the repo
```
git clone https://github.com/AV-Lab/gen0_gz_sim_ros2.git .
```
3) Build the workspace
```
cd ~/gen0_gz_sim_ros2
colcon build
```
4) Source the workspace
```
source install/setup.bash
```
5) build the gazebo plugins
```
mkdir -p ~/gen0_gz_sim_ros2/src/gz_plugins/build
cd ~/gen0_gz_sim_ros2/src/gz_plugins/build
cmake ..
make
cd ..
```
6) add the path as a gazebo system plugin 
```
export IGN_GAZEBO_SYSTEM_PLUGIN_PATH=$(pwd)/build
```

## Docker Installation
Use the ready image then refer to Quick Start Guide.
```
docker pull ghcr.io/av-lab/gen0-gz-sim-ros2:main
```

## Quick Start Guide
Make sure to source the workspace and to export the gazebo plugin (only needed on the main terminal), to avoid having to do that everytime add it to the bashrc file or use ./gzbuild.sh file provided in the repo to launch the simulation (gen0_main) but remember to give it chmod +x.

### 1) Launch the simulation and spawn the vehicle (gen0_main)
```
ros2 launch gen0_main spawn.launch.py world:=san_roundabout actors_scenario:=walking_actors3
```
Note: the launch file has the following arguments:
- world: Name of the world file (without extension) to be used in Gazebo simulation
- actors_scenario: The scenario for pedestrians (without extension to be used in Gazebo world file)
- rviz: launch rviz

### 2) Enable Interfacing with the vehicle (gen0_interface)
```
ros2 launch gen0_interface gen0_interface.launch.xml 
```

### 3) Launch the controller (gen0_controller)
```
ros2 launch gen0_controller gen0_controller.launch.xml 
```

### 4) Start the vehicle by giving it a green flag "true"
```
ros2 topic pub /planning/green_signal std_msgs/Bool "data: true" --once
```
Note: you can remove the --once flag if you want the vehicle to navigate between the stations endlessly without caring about flags.

### 5) (optional) Run the collision checker GUI
```
ros2 run gen0_controller collision_visual.py
```

### 6) (optional) Vehicle teleoperation node
```
ros2 run gen0_interface keyboard_teleop.py
```

## Development Guide

### Vehicle Interface

* Sending velocity and steering commands to the vehicle 
    1) directly through the topic "/gen0_model/command/control_cmd" the fields that are used by the sim lateral.longitudinal.speed and lateral.steering_tire_angle
    2) seperate topics "/gen0_model/speed_cmd", /gen0_model/front_left_steering, /gen0_model/front_right_steering

* Measurements of the vehicle are sent over the topics "/vehicle/status/velocity_status" and "/vehicle/status/steering_status"

* Ground truth location of the vehicle relative to lanelet_map (check TF section) is published over "/localization/kinematic_state"

### Vehicle Sensors
* The vehicle is equipped with following sensors:
    1) 3D lidar located at the front of the vehicle and the pointcloud is published over the topic "/gen0_model/front3d/lidar/points"
    2) 2D lidars located at the front right and front left of the vehicle, the scans topics are published to "/gen0_model/fl/lidar/scan" and "/gen0_model/fr/lidar/scan" respectivly

### Planner and map creation 

TBC

### World and pedestrians scenario 

TBC

### Transform tree

TBC

## Known Issues

- When adding a new link to the vehicle or removing an existing one, the localization might fail since the world ground truth is from gazebo "/gen0_model/links/poses" PoseArray topic and the index of the base_link keep on changing everytime a link has been changed inside the car. Check pose_publisher in gen0_main to update the index.

- Sometimes the pedestirans secenario does not get updated until the package has been built twice, in rare situations you will have to delete the install and build folders, and rebuild the package.

- The 3D lidar provide a pointcloud messsage which has no intenstiy values.
