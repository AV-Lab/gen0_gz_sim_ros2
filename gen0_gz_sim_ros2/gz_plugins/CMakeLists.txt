cmake_minimum_required(VERSION 3.10.2 FATAL_ERROR)

project(ActorPose)

find_package(gz-cmake3 REQUIRED)

find_package(gz-plugin2 REQUIRED COMPONENTS register)
find_package(gz-sim8 REQUIRED)

add_library(ActorPose SHARED ActorPose.cc)

set_property(TARGET ActorPose PROPERTY CXX_STANDARD 17)

target_link_libraries(ActorPose
  PRIVATE gz-plugin2::register
  PRIVATE gz-sim8::gz-sim8
)