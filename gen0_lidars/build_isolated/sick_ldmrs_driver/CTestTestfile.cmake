# CMake generated Testfile for 
# Source directory: /home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/src/sick_ldmrs_laser/sick_ldmrs_driver
# Build directory: /home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/build_isolated/sick_ldmrs_driver
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_sick_ldmrs_driver_roslaunch-check_launch "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/build_isolated/sick_ldmrs_driver/catkin_generated/env_cached.sh" "/usr/bin/python2" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/build_isolated/sick_ldmrs_driver/test_results/sick_ldmrs_driver/roslaunch-check_launch.xml" "--return-code" "/usr/bin/cmake -E make_directory /home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/build_isolated/sick_ldmrs_driver/test_results/sick_ldmrs_driver" "/opt/ros/melodic/share/roslaunch/cmake/../scripts/roslaunch-check -o \"/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/build_isolated/sick_ldmrs_driver/test_results/sick_ldmrs_driver/roslaunch-check_launch.xml\" \"/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/src/sick_ldmrs_laser/sick_ldmrs_driver/launch\" ")
subdirs("gtest")
