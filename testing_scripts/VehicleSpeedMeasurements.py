import rospy
from four_wheel_steering_msgs.msg import FourWheelSteeringStamped, FourWheelSteering
from std_msgs.msg import Header
import can
import time


pub = rospy.Publisher('four_wheel_steering', FourWheelSteeringStamped, queue_size=10)
rospy.init_node('publisher', anonymous=True)


def convert_to_decimal(odom_lsb, odom_msb, type):
    odom_lsb_binary=bin(odom_lsb)[2:].zfill(8)
    odom_msb_binary=bin(odom_msb)[2:].zfill(8)
    odom_binary=odom_msb_binary + odom_lsb_binary
    if type=='signed':
        return -(int(odom_binary, 2) & 0x8000) + (int(odom_binary, 2) & 0x7FFF)
    else:
        return int(odom_binary, 2)
        
def on_message_received(measurements):
    msg = FourWheelSteeringStamped()
    msg.header = Header()
    msg.header.stamp = rospy.Time.now()
    if measurements.arbitration_id == 0x213:
        odom_lsb = measurements.data[0]
        odom_msb = measurements.data[1]
        speed= convert_to_decimal(odom_lsb, odom_msb, 'signed') * 0.001
        msg.data.speed=speed
        pub.publish(msg)
            
if __name__ == '__main__':
    try:
        bus = can.interface.Bus(bustype='socketcan', channel='slcan0', bitrate=500000)
        # listener = can.Listener()
        # listener.on_message_received = on_message_received
        # notifier = can.Notifier(bus, [listener])
        while not rospy.is_shutdown():
            message=bus.recv()
            if message is not None:
                on_message_received(message)
    except rospy.ROSInterruptException:
        pass