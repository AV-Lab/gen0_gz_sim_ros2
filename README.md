# gen0_gz_sim_ros2

## System Rquirements 
- Ubuntu 22.04 LTS
- RAM 8GB or more
  
## Dependencies
1) ROS2 Humble
2) Gazebo ignition 6.x

## Installation
1) Create a ROS2 workspace
```
mkdir ~/gen0_gz_sim_ros2
cd gen0_gz_sim_ros2
mkdir src
cd src
```
2) Clone the repo
```
git clone https://github.com/AV-Lab/gen0_gz_sim_ros2.git
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

## Running the simulation
```
ros2 launch gen0_main spawn.launch.py 
```

