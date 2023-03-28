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


class Hardware4WS:
    def __init__(self):
        # self.bus = can.interface.Bus(bustype='socketcan',channel='slcan0', bitrate=500000)
        self.desiredSpeedAcceleration= 0.3 # m/s^2
        self.desiredSpeedDeceleration= -1.5 # m/s^2
        self.desiredSpeed= 0
        self.desiredFrontSteering= 0
        self.desiredRearSteering = 0
        # parameters used for acceleration logic as it is not handled by the vehilcle internal system
        self.acceleration= 0
        self.previousSpeed = 0
        rospy.Subscriber("four_wheel_steering_input", FourWheelSteeringStamped, self.data_callback)

    def bytesFromValue(self, step):
        hex_number = hex(step & int("1"*16, 2))
        extended_hex = "{:04x}".format(int(hex_number, 16))
        return extended_hex[2:4], extended_hex[0:2]
    
    def data_callback(self, msg):
        if msg.data.speed > abs(5.6) or msg.data.front_steering_angle > abs(0.31) or msg.data.rear_steering_angle > abs(0.31):
            print("Ignoring Input as it is exceeding the vehicle limits")
        else:
            print("Processing Input")
            self.desiredSpeed= msg.data.speed
            self.desiredFrontSteering= msg.data.front_steering_angle
            self.desiredRearSteering= msg.data.rear_steering_angle
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
        if float("{:.2f}".format(frontAngle)) != 0.31 and float("{:.2f}".format(frontAngle)) != -0.31:
            if frontAngle < hardware_4ws.desiredFrontSteering:
                frontAngle += 0.005 # radians, limited by the vehicle
            elif frontAngle > hardware_4ws.desiredFrontSteering:
                frontAngle -= 0.005

        if float("{:.2f}".format(rearAngle)) != 0.31 and float("{:.2f}".format(rearAngle)) != -0.31:
            if rearAngle < hardware_4ws.desiredRearSteering:
                rearAngle += 0.005 # radians, limited by the vehicle
            elif rearAngle > hardware_4ws.desiredRearSteering:
                rearAngle -= 0.065
                
        
        # convert to bytes format
        speed_lsb, speed_msb = hardware_4ws.bytesFromValue(int(hardware_4ws.desiredSpeed * 1000))
        acceleration_lsb, acceleration_msb = hardware_4ws.bytesFromValue(int(hardware_4ws.acceleration * 1000))
        front_steer_lsb, front_steer_msb = hardware_4ws.bytesFromValue(int(frontAngle * 10000))
        rear_steer_lsb, rear_steer_msb = hardware_4ws.bytesFromValue(int(rearAngle * 10000))

        try: 
            msg_steering = can.Message(arbitration_id=0x193, data=[int(acceleration_lsb, 16), int(acceleration_msb, 16), int(speed_lsb, 16), int(speed_msb, 16), int(front_steer_lsb, 16), int(front_steer_msb, 16), int(rear_steer_lsb, 16), int(rear_steer_msb, 16)],is_extended_id=False)
            print(msg_steering)
            # hardware_4ws.bus.send(msg_steering)
        except can.CanError:
            print("Error: message not sent")
            
        time.sleep(0.02)