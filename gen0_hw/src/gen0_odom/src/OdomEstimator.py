#!/usr/bin/python
import rospy
import math
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
import geometry_msgs
import tf
from four_wheel_steering_msgs.msg import FourWheelSteeringStamped
from std_msgs.msg import Header
import tf2_ros

class OdomEstimator:
    def __init__(self):
        # Set the wheelbase and wheel track of the robot (distance between the wheels)
        self.wheelbase = 2.8  # meters
        self.wheeltrack = 1.385  # meters

        # Initialize variables for the robot's position and orientation
        self.x = 0.0
        self.y = 0.0
        self.Psi=0.0
        self.theta = 0.0

        # Create the odometry message and set its frame IDs
        self.odom = Odometry()
        self.odom.header.frame_id = "odom"
        self.odom.child_frame_id = "baselink"

        self.odom_trans = geometry_msgs.msg.TransformStamped()

        # Create a publisher to publish the odometry data
        self.odom_pub = rospy.Publisher("odom", Odometry, queue_size=50)

        self.odom_quat = Quaternion()

        # Create a subscriber to listen for the speed, front steering, and rear steering data
        rospy.Subscriber("four_wheel_steering", FourWheelSteeringStamped, self.data_callback)

    def data_callback(self, data):
        # Extract the current time and steering angles
        current_time = data.header.stamp
        fr_steering = data.data.front_steering_angle
        re_steering = data.data.rear_steering_angle
        speed = data.data.speed
        # Calculate the time elapsed since the last update
        dt = (current_time - self.odom.header.stamp).to_sec()


        # Vx= speed*(math.cos(fr_steering) + math.cos(re_steering))/2
        # Vy= speed*(math.sin(fr_steering) + math.sin(re_steering))/2
        # yaw = -self.wheeltrack/2*math.cos(fr_steering)+ self.wheelbase/2
        Psi_prime= (speed*(math.tan(fr_steering ) - math.tan(re_steering)))/self.wheelbase
        self.Psi += Psi_prime * dt
        Vx= speed * math.cos(self.Psi)
        Vy= speed * math.sin(self.Psi)

        
        print("The current inputs are: ", Vx, Vy, Psi_prime)

        # Update the robot's position and orientation based on the linear and angular velocity
        self.x += Vx * dt
        self.y += Vy * dt
        # self.theta += angular_velocity * dt
        print("the current position: ",self.x, self.y, self.Psi)
        # Create the quaternion for the robot's orientation
        odom_quat = Quaternion(*tf.transformations.quaternion_from_euler(0, 0, self.Psi))

        # Fill in the odometry message with the current position, orientation, and velocity
        self.odom.header.stamp = current_time
        # self.odom.pose.pose.position.x= self.x
        # self.odom.pose.pose.position.y= self.y
        # self.odom.pose.pose.position.z= 0.0
        # self.odom.pose.pose.orientation=tf.transformations.quaternion_from_euler(0, 0, self.Psi)
        # self.odom.twist.twist.linear.x = Vx
        # self.odom.twist.twist.linear.y = Vy
        # self.odom.twist.twist.angular.z = Psi_prime

        self.odom.pose.pose = Pose(Point(self.x, self.y, 0.), odom_quat)
        self.odom.twist.twist = Twist(Vector3(Vx, Vy, 0), Vector3(0, 0, Psi_prime))





        self.odom_trans.header.stamp = current_time
        self.odom_trans.header.frame_id = "odom"
        self.odom_trans.child_frame_id = "baselink"
        self.odom_trans.transform.translation.x = self.x
        self.odom_trans.transform.translation.y = self.y
        self.odom_trans.transform.translation.z = 0.0
        self.odom_trans.transform.rotation = odom_quat

        odom_broadcaster = tf2_ros.StaticTransformBroadcaster()
        odom_broadcaster.sendTransform(self.odom_trans)


        # Publish the odometry message
        self.odom_pub.publish(self.odom)

if __name__ == '__main__':
    rospy.init_node('OdomEstimator', anonymous=True)
    odom_estimator = OdomEstimator()
    rospy.spin()
