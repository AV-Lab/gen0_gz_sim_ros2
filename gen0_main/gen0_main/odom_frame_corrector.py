import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped, Vector3, Quaternion
import tf2_ros
from geometry_msgs.msg import Quaternion
from tf_transformations import euler_from_quaternion, quaternion_from_euler


class OdometryCorrector(Node):
    def __init__(self):
        super().__init__('odometry_corrector')
        self.subscription = self.create_subscription(Odometry, 'gen0_model/odometry', self.odom_callback, 10)
        self.publisher = self.create_publisher(Odometry, '/localization/kinematic_state', 10)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

    def odom_callback(self, msg):
        corrected_msg = msg
        corrected_msg.header.frame_id, corrected_msg.child_frame_id = "odom", "base_link_wrong"
        corrected_msg.pose.pose.orientation=self.rotate_quaternion(msg.pose.pose.orientation, 0, 0, -1.5708)
        # self.tf_broadcaster.sendTransform(self.odom_to_transform(corrected_msg))
        self.publisher.publish(corrected_msg)


    def rotate_quaternion(self, q, roll, pitch, yaw):
        # Convert the original orientation to euler angles
        (r, p, y) = euler_from_quaternion([q.x, q.y, q.z, q.w])

        # Apply the desired rotation (rotate -pi/2 around the z-axis)
        y += yaw

        # Convert the modified euler angles back to quaternion
        rotated_quaternion = quaternion_from_euler(r, p, y)

        return Quaternion(x=rotated_quaternion[0], y=rotated_quaternion[1], z=rotated_quaternion[2], w=rotated_quaternion[3])
    

    # def odom_to_transform(self, odom_msg):
    #     transform = TransformStamped()
    #     transform.header.stamp = odom_msg.header.stamp
    #     transform.header.frame_id = odom_msg.header.frame_id
    #     transform.child_frame_id = odom_msg.child_frame_id
    #     translation = odom_msg.pose.pose.position
    #     rotation = odom_msg.pose.pose.orientation
    #     transform.transform.translation = Vector3()
    #     transform.transform.translation.x = translation.x
    #     transform.transform.translation.y = translation.y
    #     transform.transform.translation.z = translation.z
    #     transform.transform.rotation = Quaternion()
    #     transform.transform.rotation.x = rotation.x
    #     transform.transform.rotation.y = rotation.y
    #     transform.transform.rotation.z = rotation.z 
    #     transform.transform.rotation.w = rotation.w
    #     return transform

def main(args=None):
    rclpy.init(args=args)
    odom_corrector = OdometryCorrector()
    rclpy.spin(odom_corrector)
    odom_corrector.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
