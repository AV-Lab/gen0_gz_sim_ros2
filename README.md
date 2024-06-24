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
### gen0_main
```
ros2 launch gen0_main spawn.launch.py 
```
### gen0_controller
```
ros2 launch gen0_interface gen0_interface.launch.xml 
```
```
ros2 run gen0_controller PIDcontroller_CTE.py 
```
```
ros2 run gen0_controller path_loader.py 
```
```
ros2 run gen0_controller collision_checker.py
```
```
ros2 run gen0_controller PIDcontroller_velocity.py
```
```
ros2 run gen0_controller collision_visual.py
```
Start by giving the vehicle a green flag "true"
```
ros2 topic pub /planning/green_signal std_msgs/Bool "data: true" --once
```
## Path following
The controller follows a specific trajectory specified in the stations/stationx.json file to add a new station create a new file with the points and update path_loader node with the proper stations order
