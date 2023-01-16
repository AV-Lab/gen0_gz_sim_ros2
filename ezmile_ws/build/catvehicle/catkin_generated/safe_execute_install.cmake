execute_process(COMMAND "/home/riyadh/Desktop/ezmile_ws/build/catvehicle/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/riyadh/Desktop/ezmile_ws/build/catvehicle/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
