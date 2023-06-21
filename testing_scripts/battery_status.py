import can
import time

def on_message_received(msg):
    if msg.arbitration_id == 0x580:
        batter_percentage = msg.data[5]
        print("The battery percentage level is: " + str(batter_percentage))
        

bus = can.interface.Bus(bustype='socketcan', channel='slcan0', bitrate=500000)

listener = can.Listener()
listener.on_message_received = on_message_received
notifier = can.Notifier(bus, [listener])

while True:
    try:
        time.sleep(1)
    except can.CanError:
        print("cant connect to bus")


