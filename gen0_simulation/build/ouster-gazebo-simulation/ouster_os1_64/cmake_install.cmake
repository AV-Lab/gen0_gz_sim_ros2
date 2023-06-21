# Install script for directory: /home/avl-1/Documents/GitHub/ezmile_gen0/gen0_simulation/src/ouster-gazebo-simulation/ouster_os1_64

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/avl-1/Documents/GitHub/ezmile_gen0/gen0_simulation/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/avl-1/Documents/GitHub/ezmile_gen0/gen0_simulation/build/ouster-gazebo-simulation/ouster_os1_64/catkin_generated/installspace/ouster_os1_64.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ouster_os1_64/cmake" TYPE FILE FILES
    "/home/avl-1/Documents/GitHub/ezmile_gen0/gen0_simulation/build/ouster-gazebo-simulation/ouster_os1_64/catkin_generated/installspace/ouster_os1_64Config.cmake"
    "/home/avl-1/Documents/GitHub/ezmile_gen0/gen0_simulation/build/ouster-gazebo-simulation/ouster_os1_64/catkin_generated/installspace/ouster_os1_64Config-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ouster_os1_64" TYPE FILE FILES "/home/avl-1/Documents/GitHub/ezmile_gen0/gen0_simulation/src/ouster-gazebo-simulation/ouster_os1_64/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ouster_os1_64" TYPE DIRECTORY FILES "/home/avl-1/Documents/GitHub/ezmile_gen0/gen0_simulation/src/ouster-gazebo-simulation/ouster_os1_64/launch")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ouster_os1_64" TYPE DIRECTORY FILES "/home/avl-1/Documents/GitHub/ezmile_gen0/gen0_simulation/src/ouster-gazebo-simulation/ouster_os1_64/meshes")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ouster_os1_64" TYPE DIRECTORY FILES "/home/avl-1/Documents/GitHub/ezmile_gen0/gen0_simulation/src/ouster-gazebo-simulation/ouster_os1_64/urdf")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/ouster_os1_64" TYPE DIRECTORY FILES "/home/avl-1/Documents/GitHub/ezmile_gen0/gen0_simulation/src/ouster-gazebo-simulation/ouster_os1_64/worlds")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/ouster_os1_64" TYPE PROGRAM FILES "/home/avl-1/Documents/GitHub/ezmile_gen0/gen0_simulation/build/ouster-gazebo-simulation/ouster_os1_64/catkin_generated/installspace/test_ouster.py")
endif()

