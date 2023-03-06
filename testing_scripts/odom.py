import can
import time

def convert_to_decimal(odom_lsb, odom_msb, type):
    odom_lsb_binary=bin(odom_lsb)[2:].zfill(8)
    odom_msb_binary=bin(odom_msb)[2:].zfill(8)
    odom_binary=odom_msb_binary + odom_lsb_binary
    if type=='signed':
        return -(int(odom_binary, 2) & 0x8000) + (int(odom_binary, 2) & 0x7FFF)
    else:
        return int(odom_binary, 2)

def on_message_received(msg):
    if msg.arbitration_id == 0x213:
        odom_lsb = msg.data[0]
        odom_msb = msg.data[1]
        speed= convert_to_decimal(odom_lsb, odom_msb, 'signed')
        print(speed*0.001)
        

bus = can.interface.Bus(bustype='socketcan', channel='slcan0', bitrate=500000)

listener = can.Listener()
listener.on_message_received = on_message_received
notifier = can.Notifier(bus, [listener])

while True:
    try:
        time.sleep(1)
    except can.CanError:
        print("cant connect to bus")


