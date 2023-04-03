#!/usr/bin/python3

"""
This code converts the four wheel steering input to the hardware wheels of the vehicle. Note that the following are handled in this code:

1) Steering limitation by the vehicle: as the vehicle can only rotate at a speed of 0.006 radians every 20 ms (0.3 radians/second) and 
the maximum angles magnitudes are (-0.31, 0.31) radians. for simplicity I'm using 0.005 radians every 20ms instead as 0.31 isn't divisble by 60.

2) Acceleration/decelration handler, as to ensure that a positive value is sent when the targeted speed ishigher than the current speed
and that a negative value is sent when targeted speed is lower than the current speed.

3) The code neglects the previous 4WS input assuming it is still under process. The new 4WS input will be the desired goal.

"""

import can
import time
import rospy
from four_wheel_steering_msgs.msg import FourWheelSteeringStamped, FourWheelSteering
from std_msgs.msg import Header
from geometry_msgs.msg import Twist
import csv


class Hardware4WS:
    def __init__(self):
        self.bus = can.interface.Bus(bustype='socketcan',channel='slcan0', bitrate=500000)
        self.desiredSpeedAcceleration= 0.3 # m/s^2
        self.desiredSpeedDeceleration= -1.5 # m/s^2
        self.desiredSpeed= 0
        self.desiredFrontSteering= 0
        self.desiredRearSteering = 0
        # parameters used for acceleration logic as it is not handled by the vehilcle internal system
        self.acceleration= 0
        self.previousSpeed = 0
        self.file= open('/home/av-ipc/four_wheel_inputs.csv', 'a')
        self.writer = csv.writer(self.file)
        rospy.Subscriber("four_wheel_steering_input", FourWheelSteeringStamped, self.data_callback)

    def bytesFromValue(self, step):
        hex_number = hex(step & int("1"*16, 2))
        extended_hex = "{:04x}".format(int(hex_number, 16))
        return extended_hex[2:4], extended_hex[0:2]
    
    def data_callback(self, msg):
        if abs(float("{:.1f}".format(msg.data.speed))) > 5.6 or abs(float("{:.2f}".format(msg.data.front_steering_angle))) > 0.31 or abs(float("{:.2f}".format(msg.data.rear_steering_angle))) > 0.31:
            print("Ignoring Input as it is exceeding the vehicle limits")
            with open('/home/av-ipc/four_wheel_inputs.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([str(float("{:.1f}".format(msg.data.speed))), str(float("{:.2f}".format(msg.data.front_steering_angle))), str( float("{:.2f}".format(msg.data.rear_steering_angle)))])
        # print("Processing Input")
        self.desiredSpeed= min(max(float("{:.1f}".format(msg.data.speed)), -5.6), 5.6)
        self.desiredFrontSteering= min(max(float("{:.2f}".format(msg.data.front_steering_angle)), -0.31), 0.31)
        self.desiredRearSteering= min(max(float("{:.2f}".format(msg.data.rear_steering_angle)), -0.31), 0.31)
        # Acceleration/deceleration logic
        if abs(self.desiredSpeed) < abs(self.previousSpeed):
            self.acceleration= self.desiredSpeedDeceleration
        else:
            self.acceleration= self.desiredSpeedAcceleration
        self.previousSpeed=self.desiredSpeed

if __name__ == '__main__':
    rospy.init_node('hardware_4ws', anonymous=True)
    hardware_4ws = Hardware4WS()
    frontAngle= 0
    rearAngle= 0
    while not rospy.is_shutdown():
        # logic to increment the steering angle
        if frontAngle < hardware_4ws.desiredFrontSteering:
            frontAngle += 0.005 # radians, limited by the vehicle
        elif frontAngle > hardware_4ws.desiredFrontSteering:
            frontAngle -= 0.005
            
        if rearAngle < hardware_4ws.desiredRearSteering:
            rearAngle += 0.005 # radians, limited by the vehicle
        elif rearAngle > hardware_4ws.desiredRearSteering:
            rearAngle -= 0.005
        print("Desired: ", hardware_4ws.desiredFrontSteering,  hardware_4ws.desiredRearSteering)        
        print("Current: ", frontAngle, rearAngle)
        # convert to bytes format
        speed_lsb, speed_msb = hardware_4ws.bytesFromValue(int(hardware_4ws.desiredSpeed * 1000))
        acceleration_lsb, acceleration_msb = hardware_4ws.bytesFromValue(int(hardware_4ws.acceleration * 1000))
        front_steer_lsb, front_steer_msb = hardware_4ws.bytesFromValue(int(frontAngle * 10000))
        rear_steer_lsb, rear_steer_msb = hardware_4ws.bytesFromValue(int(rearAngle * 10000))

        try: 
            msg_steering = can.Message(arbitration_id=0x193, data=[int(acceleration_lsb, 16), int(acceleration_msb, 16), int(speed_lsb, 16), int(speed_msb, 16), int(front_steer_lsb, 16), int(front_steer_msb, 16), int(rear_steer_lsb, 16), int(rear_steer_msb, 16)],is_extended_id=False)
            hardware_4ws.bus.send(msg_steering)
        except can.CanError:
            print("Error: message not sent")
            
        time.sleep(0.02)