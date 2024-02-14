# gen0_gz_sim_ros2

![](/assets/images/simulation.png)

## System Rquirements 
- Ubuntu 22.04 LTS
- RAM 8GB or more
  
## Dependencies
-  ROS2 Humble
-  Gazebo ignition 6.x (Fortress for ROS2 Humble)
-  transforms3d
```
pip install transforms3d
```
-  ros-humble-tf-transformations
```
sudo apt install ros-humble-tf-transformations
```

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

