import can
import time
from pprint import pprint
from can.message import Message

def steerFrontRadToDecimal(step):
	hex_number = hex(step & int("1"*16, 2))
	extended_hex = "{:04x}".format(int(hex_number, 16))
	return extended_hex[2:4], extended_hex[0:2]

def moveVehicle(front_step, rear_step):
	current_front_step=0
	current_rear_step=0
	for i in range(1, 52):
		current_front_step= current_front_step + front_step
		front_steer_lsb, front_steer_msb= steerFrontRadToDecimal(current_front_step)
		current_rear_step= current_rear_step + rear_step
		rear_steer_lsb, rear_steer_msb= steerFrontRadToDecimal(current_rear_step)
		try:
			msg_steering = can.Message(arbitration_id=0x193,data=[0, 0, 0, 0, int(front_steer_lsb, 16), int(front_steer_msb, 16), int(rear_steer_lsb, 16), int(rear_steer_msb, 16)],is_extended_id=False)
			bus.send(msg_steering)
			time.sleep(0.02)
		except can.CanError:
			print("Message NOT sent")

bus = can.interface.Bus(bustype='socketcan',channel='slcan0', bitrate=500000)
# action= "turn_left"
action= "turn_right"


if action == "turn_right":
	moveVehicle(-60, 60) # step is 60 which is 0.006 radians (factor is 0.0001 according to the datasheet)
if action == "turn_left":
	moveVehicle(60, -60) # step is 60 which is 0.006 radians (factor is 0.0001 according to the datasheet)