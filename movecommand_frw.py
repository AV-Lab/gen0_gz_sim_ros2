import cantools
import can
import time
from pprint import pprint
from can.message import Message

#loading the dbc
db = cantools.db.load_file('/home/hassan/Desktop/EZmile/EZ10_test_LMS.dbc')

#print(db)

msg = db.get_message_by_name('PC_To_Var_1238')
#print(msg)
msg_data = msg.encode({'Command_Accel':0.3,'Command_Speed':0.2,'Front_Steer_Command':0.0,'Back_Steer_Command':0.0})

msg3 = can.Message(arbitration_id=0x214,data=[232, 3, 208, 7, 0, 0, 0, 0],is_extended_id=False)
#print(msg_data)
#print(msg3)

#sending the message
bus = can.interface.Bus(bustype='socketcan',channel='slcan0', bitrate=500000)
msg = can.Message(arbitration_id=msg.frame_id,data=msg_data,is_extended_id=False)

while True:
	try:
    		bus.send(msg)
    		time.sleep(0.02)
    		print("message sent on {}".format(bus.channel_info))
    		#print(msg)
	except can.CanError:
    		print("Message NOT sent")
