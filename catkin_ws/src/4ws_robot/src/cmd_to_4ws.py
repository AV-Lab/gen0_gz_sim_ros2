#!/usr/bin/python3

import rospy
from four_wheel_steering_msgs.msg import FourWheelSteeringStamped, FourWheelSteering
from std_msgs.msg import Header
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3

class Cmd4WS:
    def __init__(self):
        self.pub = rospy.Publisher('four_wheel_steering', FourWheelSteeringStamped, queue_size=10)
        rospy.Subscriber("cmd_vel", Twist, self.data_callback)
        self.four_wheel_steering= FourWheelSteeringStamped()

    def data_callback(self, msg):
        self.four_wheel_steering.data.speed=msg.linear.x
        self.pub.publish(self.four_wheel_steering)


if __name__ == '__main__':
    rospy.init_node('publisher', anonymous=True)
    Cmd_4WS = Cmd4WS()
    rospy.spin()