# gen0_gz_sim_ros2

gen0_gz_sim is a simulation environment currently under development for an autonomous shuttle (Gen0) at Khalifa University's SAN Campus. Built on ROS2 and Gazebo Harmonic, it features a platform with four-wheel steering control kinematics.

![](/assets/images/simulation.png)

## Table of Contents

- [System Requirements](#system-requirements)
- [Source Installation](#source-installation)
- [Docker Installation](#docker-installation)
- [Quick Start Guide](#quick-start-guide)
- [Known issues](#known-issues)
- [Integration with ORBit](#integration-with-orbit)

## System Rquirements

The system requirements depend on the world and number of pedestrians present during the runtime, furthermore, the following specifications were used to develop the simulation environement:

- Ubuntu 24.04 LTS
- RAM 64GB
- RTX 2080ti
- i9 9900k

## Source Installation

### Dependencies

- [ROS2 Jazzy](https://docs.ros.org/en/jazzy/Installation.html)
- [Gazebo Harmonic (for ROS2 Jazzy)](https://gazebosim.org/docs/harmonic/install_ubuntu)
- [san_full]() model download from the release
- colcon to build packages

```
sudo apt install python3-colcon-common-extensions
```

- ros_gz package

```
sudo apt-get install ros-jazzy-ros-gz
```

- python libraries

```
pip3 install -r requirements.txt
```

- ros-humble-tf-transformations

```
sudo apt install ros-jazzy-tf-transformations
```

### Workspace setup

1. Create a ROS2 workspace

```
mkdir ~/gen0_gz_sim_ros2
cd ~/gen0_gz_sim_ros2
mkdir src
cd src
```

2. Clone the repo

```
git clone https://github.com/AV-Lab/gen0_gz_sim_ros2.git
```

3. Move the downloaded san_full model to worlds directory

```
mv san_full.obj ~/gen0_gz_sim_ros2/src/gen0_gz_sim_ros2/gen0_gz_sim_ros2/gen0_main/worlds/san_full
```

### Building the workspace

#### Option 1: directly run gzbuild bash script (make sure to modify the workspace path inside gzbuild.sh)

```
cd gen0_gz_sim_ros2
chmod +x gzbuild.sh
./gzbuild.sh
```

#### Option 2: manually build the workspace

```
cd ~/gen0_gz_sim_ros2
colcon build
```

- Source the workspace

```
source install/setup.bash
```

- build the gazebo plugins

```
mkdir -p ~/gen0_gz_sim_ros2/src/gen0_gz_sim_ros2/gen0_gz_sim_ros2/gz_plugins/build
cd ~/gen0_gz_sim_ros2/src/gen0_gz_sim_ros2/gen0_gz_sim_ros2/gz_plugins/build
cmake ..
make
cd ..
```

- add the path as a gazebo system plugin

```
export GZ_SIM_SYSTEM_PLUGIN_PATH=$(pwd)/build
```

## Quick Start Guide

Make sure to source the workspace and to export the gazebo plugin (only needed on the main terminal), to avoid having to do that everytime add it to the bashrc file or use ./gzbuild.sh file provided in the repo to launch the simulation (gen0_main) but remember to give it chmod +x.

### 1) Launch the simulation and spawn the vehicle (gen0_main)

```
ros2 launch gen0_main spawn.launch.py world:=san_full actors_scenario:=walking_actors use_gui_config:=true
```

Note: the launch file has the following arguments:

- world: Name of the world file (without extension) to be used in Gazebo simulation
- actors_scenario: The scenario for pedestrians (without extension to be used in Gazebo world file)
- rviz: launch rviz
- use_gui_config: true → use packaged GUI (gui_teleop.config); false → use SDF/default GUI.

### 2) Enable Interfacing with the vehicle (gen0_interface)

```
ros2 run gen0_interface cmdvel_to_vehicle.py
```

### 3) Door & Ramp control (gen0_main)

Open sequence (door → ramp after delay):

```bash
ros2 launch gen0_main door_ramp_control.launch.py action:=open
```

Close sequence (ramp → door after delay):

```bash
ros2 launch gen0_main door_ramp_control.launch.py action:=close
```

> `action` defaults to `open` if not provided.


## Known Issues

- When adding a new link to the vehicle or removing an existing one, the localization might fail since the world ground truth is from gazebo "/gen0_model/links/poses" PoseArray topic and the index of the base_link keep on changing everytime a link has been changed inside the car. Check pose_publisher in gen0_main to update the index.

- Sometimes the pedestirans secenario does not get updated until the package has been built twice, in rare situations you will have to delete the install and build folders, and rebuild the package.

## Integration with ORBit

- Refer to the guide available at [avlab knowledge base](https://kb.avlab.io/20-DevOps/21-Software%20Dev/21.1-ORBit/) for integration instructions.
