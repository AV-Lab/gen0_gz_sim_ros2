import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped, Vector3, Quaternion, PoseArray
from nav_msgs.msg import Odometry
import tf2_ros
from geometry_msgs.msg import Quaternion
from tf_transformations import euler_from_quaternion, quaternion_from_euler


class GroundTruthPublisher(Node):
    def __init__(self):
        super().__init__('pose_publisher')
        self.subscription = self.create_subscription(PoseArray, '/gen0_model/pose', self.pose_callback, 10)
        self.publisher = self.create_publisher(Odometry, '/localization/kinematic_state', 10)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        self.location= Odometry()

    def pose_callback(self, msg):
        self.location.header.stamp= self.get_clock().now().to_msg()
        self.location.header.frame_id, self.location.child_frame_id = "map", "base_link"
        # Below constants are the position/orientation transform between gazebo world and the autoware map, index 12 is the position of vehicle from gz
        self.location.pose.pose.orientation=self.rotate_quaternion(msg.poses[12].orientation, 0, 0, -2.57079632679)
        self.location.pose.pose.position.x= 25.00 + msg.poses[12].position.x
        self.location.pose.pose.position.y= -13.5288 + msg.poses[12].position.y
        self.location.pose.pose.position.z= -2.985617160797119
        self.tf_broadcaster.sendTransform(self.pose_to_transform(self.location))
        self.publisher.publish(self.location)


    def rotate_quaternion(self, q, roll, pitch, yaw):
        # Convert the original orientation to euler angles
        (r, p, y) = euler_from_quaternion([q.x, q.y, q.z, q.w])

        # Apply the desired rotation (rotate -pi/2 around the z-axis)
        y += yaw

        # Convert the modified euler angles back to quaternion
        rotated_quaternion = quaternion_from_euler(r, p, y)

        return Quaternion(x=rotated_quaternion[0], y=rotated_quaternion[1], z=rotated_quaternion[2], w=rotated_quaternion[3])
    

    def pose_to_transform(self, location_msg):
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = "map"
        transform.child_frame_id = "base_link"
        translation = location_msg.pose.pose.position
        rotation = location_msg.pose.pose.orientation
        transform.transform.translation = Vector3()
        transform.transform.translation.x = translation.x
        transform.transform.translation.y = translation.y
        transform.transform.translation.z = translation.z
        transform.transform.rotation = Quaternion()
        transform.transform.rotation.x = rotation.x
        transform.transform.rotation.y = rotation.y
        transform.transform.rotation.z = rotation.z 
        transform.transform.rotation.w = rotation.w
        return transform

def main(args=None):
    rclpy.init(args=args)
    pose_publisher = GroundTruthPublisher()
    rclpy.spin(pose_publisher)
    pose_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
