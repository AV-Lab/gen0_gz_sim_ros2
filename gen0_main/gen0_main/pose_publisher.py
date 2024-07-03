#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped, Vector3, Quaternion, PoseArray, PoseStamped
from nav_msgs.msg import Odometry
import tf2_ros
from geometry_msgs.msg import Quaternion
import tf2_geometry_msgs

class GroundTruthPublisher(Node):
    def __init__(self):
        super().__init__('pose_publisher')
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        # wait for transform world -> map to appear
        while not self.tf_buffer.can_transform('lanelet_map', 'world', rclpy.time.Time().to_msg()):
            self.get_logger().info("Waiting for transform...")
            rclpy.spin_once(self)  # Spin once to process events
        self.subscription = self.create_subscription(PoseArray, '/gen0_model/links/poses', self.pose_callback, 10)
        self.publisher = self.create_publisher(Odometry, '/localization/kinematic_state', 10)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        self.world_pose= PoseStamped()
        self.location= Odometry()

    def pose_callback(self, msg):
        '''
        Need to create a PoseStamped message out of the PoseArray that we receive since on the developemnt date tf2_ros.Buffer().transform 
        still does not accept the message type tf2_geometry_msgs, however it accepts PoseStamped messages
        '''
        self.world_pose.header.frame_id= 'world'
        self.world_pose.pose.position= msg.poses[12].position
        self.world_pose.pose.orientation= msg.poses[12].orientation

        # Create an odom message of location relative to map frame
        self.location.header.stamp= self.get_clock().now().to_msg()
        self.location.header.frame_id, self.location.child_frame_id = "lanelet_map", "odom"
        # transform from odom to map by using odom to world (gazebo ground truth)
        position_odom_map = self.tf_buffer.transform(self.world_pose, 'lanelet_map')
        self.location.pose.pose.orientation=position_odom_map.pose.orientation
        self.location.pose.pose.position= position_odom_map.pose.position
        self.location.pose.pose.position.z = self.location.pose.pose.position.z -5.79225126837 # keep the z fixed because the lanlent is designed that way -2.9453 
        self.tf_broadcaster.sendTransform(self.pose_to_transform(self.location))
        self.publisher.publish(self.location)
    
    def pose_to_transform(self, location_msg):
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = "lanelet_map"
        transform.child_frame_id = "odom"
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
