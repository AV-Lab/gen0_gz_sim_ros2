import cantools
import can
import time
from pprint import pprint
from can.message import Message

#loading the dbc
db = cantools.db.load_file('/home/hassan/Desktop/EZmile/EZ10_test_LMS.dbc')

#print(db)

msg = db.get_message_by_name('PC_To_Var_1310')
#print(msg)
msg_data = msg.encode({'PC_CAN_Left_Blinker':0,'PC_CAN_Right_Blinker':0,'PC_CAN_Hazard_Warning_Lights':0,'PC_CAN_Config_Param':0,'PC_CAN_PAR_Warning_On_Null_Speed':0,'PC_CAN_PAR_Use_Ramp':0,'PC_CAN_PAR_Use_Led_Column':0})
#print(msg_data)

#sending the message
bus = can.interface.Bus(bustype='socketcan',channel='slcan0', bitrate=500000)
msg = can.Message(arbitration_id=msg.frame_id,data=msg_data,is_extended_id=False)
while True:
	try:
    		bus.send(msg)
    		print("message sent on {}".format(bus.channel_info))
    		time.sleep(0.01)
    		#print(msg)
    
	except can.CanError:
    		print("Message NOT sent")
