# EZmile-Gen0

## *** EZmile-Gen0 Simulation ***
This section provides instructions on how to run the simulation of the vehicle. It is highly recommended to run the simulation on a computer system with Ubuntu 20.04 operating system installed. In addition, it is also recommended to use the ROS Noetic distribution. as it has been tested and found to work optimally on this particular setup.

### 1) Installation

**ROS Packages**
```
# You can run the rospackages.sh file via terminal which contains all requried ros packages (noetic) 
cd ezmile_gen0
sudo chmod +x rospackages.sh
./rospackages.sh
```
**Install dependencies**
```
cd gen0_simulation
rosdep install --from-paths src --ignore-src -r -y
```
**lightsfm package build**
```
cd src/lightsfm
make
sudo make install
```
**Build & source the workspace**
```
cd gen0_simulation
catkin_make
source devel/setup.bash
```
### 2) Running the Simulation

**Spawn the vehicle in a small city world**
```
roslaunch gen0_4ws spawn.launch
```
The launch file will start the following: 
1) spawn.launch which spawns the vehicle and its releative Xacros/Urdfs
2) points_to_scan as the ouster lidar produces pointcloud which gets converted to scan
3) Gazebo Simulator
4) Rviz for visualization 

```
roslaunch gen0_4ws gen0_cmd_odom.launch 
```
This file launches Odom estimator based on speed measurements from wheel encoders (gazebo velocity topic in this case) and cmd to 4ws conversion nodes.

```
roslaunch gen0_4ws gen0_move_base.launch 
```
This file launches the move base node alongside TEB planner.

**Set a navigation goal on RVIZ**

![](/assets/images/gen0_rviz.png)

**Optional: to run gmapping in a new .world file**

1) Update world_name variable in the spawn.launch file to the new world created 
```
<arg name="world_name" value="$(find gen0_4ws)/worlds/****.world"/>
```
2) Save and run spawn launch file
```
roslaunch gen0_4ws spawn.launch
```
3) Run the odom estimator and four wheel steering conversions nodes
```
roslaunch gen0_4ws gen0_cmd_odom.launch 
```
4) Run the gmapping launch file
```
roslaunch gen0_4ws gen0_gmapping.launch
```
5) Move the vehicle around by writing to cmd_vel topic

6) Save the map
```
rosrun map_server map_saver -f my_map
```
**Optional: Add more pedestrians to the world**
1) Open the .world file you want to modify
2) Add the following tag
```
<actor name="actor1">
  <pose>2 3 1.213800 0 0 0</pose>
  <skin>
    <filename>moonwalk.dae</filename>
    <scale>1.0</scale>
  </skin>
  <animation name="walking">
    <filename>walk.dae</filename>
    <scale>1.000000</scale>
    <interpolate_x>true</interpolate_x>
  </animation>
  <!-- plugin definition -->
  <plugin name="actor1_plugin" filename="libPedestrianSFMPlugin.so">
    <velocity>1</velocity>
    <radius>0.4</radius>
    <animation_factor>5.1</animation_factor>
    <people_distance>6.0</people_distance>
    <!-- weights -->
    <goal_weight>2.0</goal_weight>
    <obstacle_weight>80.0</obstacle_weight>
    <social_weight>15</social_weight>
    <group_gaze_weight>3.0</group_gaze_weight>
    <group_coh_weight>2.0</group_coh_weight>
    <group_rep_weight>1.0</group_rep_weight>
    <ignore_obstacles>
      <model>ground_plane</model>
      <model>sidewalk_16</model>
    </ignore_obstacles>
    <trajectory>
      <cyclic>true</cyclic>
      <waypoint>40 8 1.213800</waypoint>
      <waypoint>40 -8 1.213800</waypoint>
    </trajectory>
  </plugin>
  </actor>
```
3) Modify the way points for the pedestrian path


## *** EZmile-Gen0 Hardware ***

This section provides instructions on how to launch vehicle hardware codes, how to create a map using SLAM gmapping and autonomous navigation using TEB planner. The vehicle hardware currently works on ROS Melodic verion.

### 1) Installation

**ROS Packages**
```
# You can run the rospackages.sh file via terminal which contains all requried ros packages (noetic) 
cd ezmile_gen0
sudo chmod +x rospackages.sh
./rospackages.sh
```

**Building the workspaces**
gen0_hw workspace
```
cd gen0_hardware/gen0_hw
catkin_make
```
gen0_lidars workspace
```
cd gen0_hardware/gen0_lidars
catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release
```
Make sure to source the correct workspace based on which package you want to run:
```
source devel/setup.bash
```
or for gen0_lidars
```
source devel_isolated/setup.bash
```

### 2) Setup CAN bus communication
run the following in terminal:
```
cd gen0_hardware
./can_setup.sh
```
if the USB port is not recognized then it must be changed inside the file:
```
sudo nano can_setup.sh
```
modify /dev/ttyUSBX to the right port. Make sure to run can_setup file until it shows no port error, then CAN bus should be ready to use.

### 3) Launch the vehicle base codes

**Vehicle Main Launch (URDF, transforms and RVIZ). Workspace: gen0_hw**
```
roslaunch gen0_main main.launch
```
**Vehicle 2d navgiation lidars. Workspace: gen0_hw**
```
roslaunch lms1xx LMS1xx.launch
```
**Vehicle 3d localization lidars. Workspace: gen0_lidars**
```
roslaunch sick_ldmrs_driver sick_ldmrs_node.launch
```
**Vehicle points to scan conversion and merger Workspace: gen0_hw**
```
roslaunch gen0_main points_to_scan.launch
roslaunch ira_laser_tools laserscan_multi_merger.launch
```
**Vehicle odom estimator Workspace: gen0_hw**
```
roslaunch gen0_odom odom_estimator.launch
rosrun gen0_main Hardware4WS.py 
```

### 4) Launch TEB Planner
**Vehicle move_base and cmd convertor Workspace: gen0_hw**
```
roslaunch gen0_main gen0_move_base.launch 
rosrun gen0_main cmd_to_4ws.py
```
at this point RVIZ might still show no transformation. All you need to do is to release the emergency from the manual controller inside the vehicle and rearm the vehicle. RVIZ should start showing lidar readings and the vehicle 3d model.

### 5) Map Creation
Alternativly if you want to create a new map, launch the vehicle base codes and then launch the following:

**Vehicle SLAM Gmapping Workspace: gen0_hw**
```
roslaunch gen0_main gen0_gmapping.launch
```
After moving the vehicle around to get capture a map you can save the map using the following:
```
rosrun map_server map_saver -f my_map
```
Modify the map file name in gen0_move_base.launch, update args="$(find gen0_main)/maps/san_parking.yaml" to the right file name.


## *** EZmile-Gen0 Communication ***

This segment will explain about starting hardware communication with EZmile Gen 0, there are however requirements that need to be met before communication is initiated:

initiating communication with EZmile 


**Requirementes:**

  1. LAWICEL AB canusb (model T70+) hardware
  2. install [cantools lib](https://pypi.org/project/cantools/) 
  3. install [can-utils lib](https://github.com/linux-can/can-utils)
  4. install linux drivers from ftdi, VCP, D2XX, D3XX [FTDI drivers](https://ftdichip.com/drivers/) "might not be needed"
  5. reference documents, EZmile files and documents: Gen0 automatic mode command description, LMS CAN interface definition document
  6. needed document: EZmile LMS dbc file
  
  
**Procedure to initiate communication with the vehicle:**

  first of all make sure the vehicle is in manual mode on both the external and internal panels.
  
    1. turn on vehicle using the outer red knob
    2. turn the switch from arriv to mar in the outside hatch
    3. make sure both switched are set to manual
    4. connect usb to laptop/IPC
    5. establish connection using the first set of commands
    6. Rearm vehicle and wait for bell sound
    7. send heartbeat signal
    8. optional: send config param signal
    9. switch to auto mode from outside
    10. switch the activ then the auto mode in the inside hatch
    11. press the door button then wait for the emergency light to on ready
    12. rearm the vehicle
    13. send movement command while the car is rearming, the command should be on while the vehicle is in auto mode
	  
  the linux commands file include the commands needed for this operation and the python files are needed to send commands
  
  remark: make sure to update the file path of dbc file inside the python files
