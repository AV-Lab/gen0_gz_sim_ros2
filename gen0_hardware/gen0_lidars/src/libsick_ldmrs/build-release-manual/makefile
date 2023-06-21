#
# Makefile for the LD-MRS example application
#
# 04.03.2014, SICK AG, willhvo
#

TOOLCHAIN_PATH = 
ROOTFS_PATH    = 
CROSS_COMPILE  = 
PREFIX         = $(ROOTFS_PATH)

#
# macros
# Make sure, that CROSS_COMPILE contains the compiler prefix for cross compile!
#
AS      = $(CROSS_COMPILE)as
LD      = $(CROSS_COMPILE)ld
CC      = $(CROSS_COMPILE)gcc
CPP     = $(CC) -E
CXX     = $(CROSS_COMPILE)g++
AR      = $(CROSS_COMPILE)ar
NM      = $(CROSS_COMPILE)nm
STRIP   = $(CROSS_COMPILE)strip
OBJCOPY = $(CROSS_COMPILE)objcopy
OBJDUMP = $(CROSS_COMPILE)objdump
RM      = rm -f
MAKEDIR = mkdir -p
COPY    = cp -rf

CFLAGS  = -Wall
# Linker options. Note that older GCC compilers include the
# pthread library with "-lpthread".
LIBS   := -L$(PREFIX)/lib \
          -L$(PREFIX)/usr/lib \
          -pthread

AFLAGS := -D__ASSEMBLY__

#
# Include paths
# Make sure, that PREFIX points to your rootfs and INCLUDE points to the
# compiler include path for cross compile!
#
ifdef INCLUDE
  export INC = -I$(INCLUDE) \
               -I$(PREFIX)/usr/include \
               -I$(PREFIX)/usr/src/linux/include
else
  export INC = -I$(PREFIX)/usr/include \
               -I$(PREFIX)/usr/src/linux/include
endif

# Die Dateien des Projekts
# Header
HEADERS := $(wildcard ../*.h ../src/*.h)
#SOURCES := $(wildcard ../*.cpp ../src/*.cpp)
# Source
SOURCES := ../src/main.cpp \
			../src/manager.cpp \
			../src/datatypes/Line2D.cpp \
			../src/datatypes/Box2D.cpp \
			../src/datatypes/Msg.cpp \
			../src/datatypes/Point2D.cpp \
			../src/datatypes/Point3D.cpp \
			../src/datatypes/Ellipse2D.cpp \
			../src/datatypes/Circle2D.cpp \
			../src/datatypes/Polygon2D.cpp \
			../src/datatypes/Polygon3D.cpp \
			../src/datatypes/Position3D.cpp \
			../src/datatypes/PositionWGS84.cpp \
			../src/datatypes/Trigger.cpp \
			../src/datatypes/Scan.cpp \
			../src/datatypes/ScanPoint.cpp \
			../src/datatypes/ScannerInfo.cpp \
			../src/datatypes/SensorStateInfo.cpp \
			../src/datatypes/Object.cpp \
			../src/datatypes/EvalCase.cpp \
			../src/datatypes/EvalCases.cpp \
			../src/datatypes/EvalCaseResult.cpp \
			../src/datatypes/EvalCaseResults.cpp \
			../src/datatypes/FieldDescription.cpp \
			../src/datatypes/FieldParameter.cpp \
			../src/datatypes/Fields.cpp \
			../src/datatypes/Measurement.cpp \
			../src/interfaces/tcp.cpp \
			../src/interfaces/file.cpp \
			../src/tools/errorhandler.cpp \
			../src/tools/BasicDataBuffer.cpp \
			../src/tools/MathToolbox.cpp \
			../src/tools/Mutex.cpp \
			../src/tools/SickThread.cpp \
			../src/tools/Time.cpp \
			../src/tools/Timer.cpp \
			../src/tools/toolbox.cpp \
			../src/tools/WatchdogTimer.cpp \
			../src/devices/BasicDevice.cpp \
			../src/devices/LD_MRS.cpp \
			../src/devices/LuxBase.cpp \
			../src/application/BasicApplication.cpp \
			../src/application/LdmrsApp.cpp \
			../src/application/LdmrsSectorChangeApp.cpp \
			../src/application/LdmrsFieldApp.cpp \
			../src/application/LdmrsNtpTimeApp.cpp \
			../src/application/LdmrsScanpointCoordinateApp.cpp \
			../src/sopas/colaa.cpp \
			../src/sopas/colab.cpp \
			../src/sopas/LdmrsSopasLayer.cpp \
			../src/sopas/SopasBase.cpp

OBJS := $(SOURCES:.cpp=.o)
# Output file ("Binary")
BIN := LdmrsExample.release


#
# Rules
#
all : $(BIN)

# Aufraeumen
.PHONY: clean
clean :
	${RM} $(OBJS)
	${RM} $(BIN)

	
#
# These are the rules for building the binaries of a
# C++ applications.
#

#-g fuer debug
.cpp.o : $(HEADERS)
	$(CXX) -c $(INC) $(CFLAGS) $< -o $@
	
$(BIN) : $(OBJS)
	$(CXX) -g $(INC) $(CFLAGS) $(LIBS) $(OBJS) -o $@

