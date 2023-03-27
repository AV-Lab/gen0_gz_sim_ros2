import can
import time
import rospy
from four_wheel_steering_msgs.msg import FourWheelSteeringStamped, FourWheelSteering
from std_msgs.msg import Header
from geometry_msgs.msg import Twist


class Hardware4WS:
    def __init__(self):
        self.bus = can.interface.Bus(bustype='socketcan',channel='slcan0', bitrate=500000)
        self.desiredSpeedAcceleration= 0.3 # m/s^2
        self.desiredSpeedDeceleration= -1.5 # m/s^2
        rospy.Subscriber("four_wheel_steering_input", FourWheelSteeringStamped, self.data_callback)

    def steerFrontRadToDecimal(self, step):
        hex_number = hex(step & int("1"*16, 2))
        extended_hex = "{:04x}".format(int(hex_number, 16))
        return extended_hex[2:4], extended_hex[0:2]
    
    def data_callback(self, msg):
        if msg.data.speed > abs(5.6) or msg.data.front_steering_angle > abs(0.31) or msg.data.rear_steering_angle > abs(0.31):
            print("Ignoring Input as it is exceeding the vehicle limits")
        else:
            print("Processing Input")
            front_steer_lsb, front_steer_msb = self.steerFrontRadToDecimal(msg.data.front_steering_angle * 10000)
            rear_steer_lsb, rear_steer_msb = self.steerFrontRadToDecimal(msg.data.rear_steering_angle * 10000)
            speed_lsb, speed_msb = self.steerFrontRadToDecimal(int(msg.data.speed * 1000))
            try: 
                msg_steering = can.Message(arbitration_id=0x193, data=[int(self.acceleration_lsb, 16), int(self.acceleration_msb, 16), int(self.speed_lsb, 16), int(self.speed_msb, 16), int(self.front_steer_lsb, 16), int(self.front_steer_msb, 16), int(self.rear_steer_lsb, 16), int(self.rear_steer_msb, 16)],is_extended_id=False)
                print(msg_steering)
                # self.bus.send(msg_steering)
            except can.CanError:
                print("Message NOT sent")

if __name__ == '__main__':
    rospy.init_node('hardware_4ws', anonymous=True)
    hardware_4ws = Hardware4WS()
    rospy.spin()