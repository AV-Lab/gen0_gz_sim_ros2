# Install script for directory: /home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/src/libsick_ldmrs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
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

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated/lib/cmake/SickLDMRS/SickLDMRSConfig.cmake;/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated/lib/cmake/SickLDMRS/SickLDMRSConfigVersion.cmake")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated/lib/cmake/SickLDMRS" TYPE FILE FILES
    "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/build_isolated/libsick_ldmrs/install/CMakeFiles/SickLDMRSConfig.cmake"
    "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/build_isolated/libsick_ldmrs/install/SickLDMRSConfigVersion.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xdevx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated/lib/cmake/SickLDMRS/SickLDMRSTargets.cmake")
    file(DIFFERENT EXPORT_FILE_CHANGED FILES
         "$ENV{DESTDIR}/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated/lib/cmake/SickLDMRS/SickLDMRSTargets.cmake"
         "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/build_isolated/libsick_ldmrs/install/CMakeFiles/Export/_home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated/lib/cmake/SickLDMRS/SickLDMRSTargets.cmake")
    if(EXPORT_FILE_CHANGED)
      file(GLOB OLD_CONFIG_FILES "$ENV{DESTDIR}/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated/lib/cmake/SickLDMRS/SickLDMRSTargets-*.cmake")
      if(OLD_CONFIG_FILES)
        message(STATUS "Old export file \"$ENV{DESTDIR}/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated/lib/cmake/SickLDMRS/SickLDMRSTargets.cmake\" will be replaced.  Removing files [${OLD_CONFIG_FILES}].")
        file(REMOVE ${OLD_CONFIG_FILES})
      endif()
    endif()
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated/lib/cmake/SickLDMRS/SickLDMRSTargets.cmake")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated/lib/cmake/SickLDMRS" TYPE FILE FILES "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/build_isolated/libsick_ldmrs/install/CMakeFiles/Export/_home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated/lib/cmake/SickLDMRS/SickLDMRSTargets.cmake")
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
     "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated/lib/cmake/SickLDMRS/SickLDMRSTargets-release.cmake")
    if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
        message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
    endif()
    if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
        message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
    endif()
file(INSTALL DESTINATION "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated/lib/cmake/SickLDMRS" TYPE FILE FILES "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/build_isolated/libsick_ldmrs/install/CMakeFiles/Export/_home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/install_isolated/lib/cmake/SickLDMRS/SickLDMRSTargets-release.cmake")
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/sick_ldmrs" TYPE FILE FILES "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/src/libsick_ldmrs/package.xml")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/build_isolated/libsick_ldmrs/install/src/cmake_install.cmake")

endif()

if(CMAKE_INSTALL_COMPONENT)
  set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
file(WRITE "/home/av-ipc/Documents/GitHub/ezmile_gen0/gen0_lidars/build_isolated/libsick_ldmrs/install/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
