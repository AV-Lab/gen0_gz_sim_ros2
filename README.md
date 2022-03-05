# EZmile-Gen-0
initiating communication with EZmile 


This segment will explain about starting communication with EZmile Gen 0, there are however requirements that need to be met before communication is initiated:

## Requirementes:

  1. LAWICEL AB canusb (model T70+) hardware
  2. install [cantools lib](https://pypi.org/project/cantools/) 
  3. install [can-utils lib](https://github.com/linux-can/can-utils)
  4. install linux drivers from ftdi, VCP, D2XX, D3XX [FTDI drivers](https://ftdichip.com/drivers/) "might not be needed"
  5. reference documents, EZmile files and documents: Gen0 automatic mode command description, LMS CAN interface definition document
  6. needed document: EZmile LMS dbc file
  
  
## Procedure to initiate communication with the vehicle:

  first of all make sure the vehicle is in manual mode on both the external and internal panels.
  
    1. turn on vehicle using the outer red knob
    2. turn the switch from arriv to mar in the outside hatch
    3. make sure both switched are set to manual
    4. connect usb to laptop
    5. establish connection using the first set of commands
    6. Rearm vehicle and wait for bell sound
    7. send heartbeat signal
    8. optional: send config param signal
    9. switch to auto mode from outside
    10. switch the activ then the auto mode in the inside hatch
    11. press the door button then wait for the emergency light to on ready
    12. rearm the vehicle
    13. send movement command
	  
  the linux commands file include the commands needed for this operation and the python files are needed to send commands
  
  remark: make sure to update the file path of dbc file inside the python files
