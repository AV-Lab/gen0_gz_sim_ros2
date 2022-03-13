import cantools
import can
import time
from pprint import pprint
from can.message import Message

#loading the dbc
db = cantools.db.load_file('/home/hassan/Desktop/EZmile/EZ10_test_LMS.dbc')

#print(db)

msg = db.get_message_by_name('PC_To_PLC_214')
msg2 = db.get_message_by_name('PC_To_PLC_214')
#print(msg)
msg_data = msg.encode({'AutoDoorRequest':0,'AutoRampRequest':0,'StopStation':0,'AutoEstop':1,'PedestrianAlert':0,'HeadLight_Flash_Request':0,'c_Estop_PCNav_Not_Requested':1})
msg2_data = msg2.encode({'AutoDoorRequest':0,'AutoRampRequest':0,'StopStation':0,'AutoEstop':0,'PedestrianAlert':0,'HeadLight_Flash_Request':0,'c_Estop_PCNav_Not_Requested':1})
#print(msg_data)
#msg3 = can.Message(arbitration_id=0x214,data=[136, 0, 0, 0, 0, 0, 0, 0],is_extended_id=False)
#msg4 = can.Message(arbitration_id=0x214,data=[128, 0, 0, 0, 0, 0, 0, 0],is_extended_id=False)

#msg5 = can.Message(arbitration_id=0x193,data=[244, 1, 0, 0, 0, 0, 0, 0],is_extended_id=False)
#msg6 = can.Message(arbitration_id=0x293,data=[0, 0, 0, 0, 0, 0, 0, 0],is_extended_id=False)

msg = can.Message(arbitration_id=msg.frame_id,data=msg_data,is_extended_id=False)
msg2 = can.Message(arbitration_id=msg2.frame_id,data=msg2_data,is_extended_id=False)

#print(msg)
#print(msg2)
#print(msg3)
#print(msg4)
#print(msg5)
#print(msg6)

#sending the message
bus = can.interface.Bus(bustype='socketcan',channel='slcan0', bitrate=500000)
while True: 
	try:
	    bus.send(msg)
	    #bus.send(msg5)
	    #bus.send(msg6)
	    print("message sent on {}".format(bus.channel_info))
	    time.sleep(0.05)
	    bus.send(msg2)
	    time.sleep(0.05) 
	except can.CanError:
	    print("Message NOT sent")  
	     
#	try:
#	    bus.send(msg2)
	    #bus.send(msg5)
	    #bus.send(msg6)
#	    print("message sent on {}".format(bus.channel_info))
	    #print(msg)
#	    time.sleep(0.05)
#	except can.CanError:
#	    print("Message NOT sent")
