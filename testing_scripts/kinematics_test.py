import rospy
from four_wheel_steering_msgs.msg import FourWheelSteeringStamped, FourWheelSteering
from std_msgs.msg import Header
import time


pub = rospy.Publisher('four_wheel_steering', FourWheelSteeringStamped, queue_size=10)
rospy.init_node('publisher', anonymous=True)
            
if __name__ == '__main__':
    for i in range(10):
        msg = FourWheelSteeringStamped()
        msg.header = Header()
        msg.header.stamp = rospy.Time.now()
        msg.data.speed= 1
        msg.data.front_steering_angle=1.5708
        msg.data.rear_steering_angle=1.5708
        pub.publish(msg)
        time.sleep(1)

