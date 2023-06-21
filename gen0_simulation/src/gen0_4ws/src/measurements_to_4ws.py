#!/usr/bin/python3

import rospy
from four_wheel_steering_msgs.msg import FourWheelSteeringStamped
from std_msgs.msg import Header
from geometry_msgs.msg import Twist
import math
from sensor_msgs.msg import JointState
from gazebo_msgs.srv import GetModelState, GetModelStateRequest

class Measurements4WS:
    def __init__(self):
        self.pub = rospy.Publisher('four_wheel_steering_measurements', FourWheelSteeringStamped, queue_size=50)

        self.get_model_state = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
        self.request = GetModelStateRequest()
        self.request.model_name = 'four_wheel_opposite_steering' 
        rospy.Subscriber("/4ws/joint_states", JointState, self.data_callback)
        self.four_wheel_steering= FourWheelSteeringStamped()
        self.header= Header()
        self.wheelbase= 2.8

    def data_callback(self, msg):
        id_back=msg.name.index("back_left_steering_joint") # we dont need to check the right joints because its always the same as the left
        id_front=msg.name.index("front_left_steering_joint") # front and back always have the same magnitude but opposite in sign 
        id_sign=msg.name.index("back_left_wheel_joint") # to know which direction is the speed

        response = self.get_model_state(self.request)
        vx=response.twist.linear.x
        vy=response.twist.linear.y
        speed=math.sqrt(vx**2 + vy**2)
        if speed < 0.01:# ignore speed if the value is too small. otherwise it will accmulate with odom
            speed=0 

        self.four_wheel_steering.header=self.header
        self.four_wheel_steering.data.speed=math.copysign(speed, msg.velocity[id_sign])
        self.four_wheel_steering.data.front_steering_angle=msg.position[id_front]
        self.four_wheel_steering.data.rear_steering_angle= msg.position[id_back]

        self.header.stamp= rospy.Time.now()
        self.pub.publish(self.four_wheel_steering)


if __name__ == '__main__':
    rospy.init_node('measurements_4ws', anonymous=True)
    measurements_4WS = Measurements4WS()
    rospy.spin()