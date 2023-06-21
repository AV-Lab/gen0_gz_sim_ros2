#!/usr/bin/python3

import rospy
from four_wheel_steering_msgs.msg import FourWheelSteeringStamped, FourWheelSteering
from std_msgs.msg import Header
import can
import time


pub = rospy.Publisher('four_wheel_steering_measurements', FourWheelSteeringStamped, queue_size=10)
rospy.init_node('four_wheel_steering_publisher', anonymous=True)


def convert_to_decimal(lsb, msb, type):
    lsb_binary=bin(lsb)[2:].zfill(8)
    msb_binary=bin(msb)[2:].zfill(8)
    binary=msb_binary + lsb_binary
    if type=='signed':
        return -(int(binary, 2) & 0x8000) + (int(binary, 2) & 0x7FFF)
    else:
        return int(binary, 2)
        
def on_message_received(measurements):
    msg = FourWheelSteeringStamped()
    msg.header = Header()
    msg.header.stamp = rospy.Time.now()
    if measurements.arbitration_id == 0x213:
        # Speed
        speed_lsb = measurements.data[0]
        speed_msb = measurements.data[1]
        speed= convert_to_decimal(speed_lsb, speed_msb, 'signed') * 0.001
        # front steering
        fs_lsb = measurements.data[2]
        fs_msb = measurements.data[3]
        fs= convert_to_decimal(fs_lsb, fs_msb, 'signed') * 0.0001
        # rear steering
        rs_lsb = measurements.data[4]
        rs_msb = measurements.data[5]
        rs= convert_to_decimal(rs_lsb, rs_msb, 'signed') * 0.0001

        msg.data.speed=speed
        msg.data.front_steering_angle=fs
        msg.data.rear_steering_angle= rs
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