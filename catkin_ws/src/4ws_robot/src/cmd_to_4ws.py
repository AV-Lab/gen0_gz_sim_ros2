#!/usr/bin/python3

import rospy
from four_wheel_steering_msgs.msg import FourWheelSteeringStamped, FourWheelSteering
from std_msgs.msg import Header
from geometry_msgs.msg import Twist
import math

class Cmd4WS:
    def __init__(self):
        self.pub = rospy.Publisher('four_wheel_steering_input', FourWheelSteeringStamped, queue_size=10)
        rospy.Subscriber("cmd_vel", Twist, self.data_callback)
        self.four_wheel_steering= FourWheelSteeringStamped()
        self.header= Header()
        self.wheelbase= 2.8

    def data_callback(self, msg):
        v= msg.linear.x # linear velocity
        omega= msg.angular.z # angular velocity

        # Check if v/omega is doable (0/0) scenario is forbidden 
        try:
            r= v/omega # turning radius
        except:
            delta_f= 0 # no turning
        else:
            delta_f= math.atan(self.wheelbase/(2*r))

        delta_r= -delta_f
        self.header.stamp= rospy.Time.now()
        self.four_wheel_steering.header=self.header
        self.four_wheel_steering.data.speed=msg.linear.x
        self.four_wheel_steering.data.front_steering_angle=delta_f
        self.four_wheel_steering.data.rear_steering_angle= delta_r
        self.pub.publish(self.four_wheel_steering)


if __name__ == '__main__':
    rospy.init_node('cmd_to_4ws', anonymous=True)
    Cmd_4WS = Cmd4WS()
    rospy.spin()