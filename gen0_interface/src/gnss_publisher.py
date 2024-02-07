#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped
from std_msgs.msg import Header

class GNSSPublisher(Node):
    def __init__(self):
        super().__init__('pose_publisher')
        self.publisher = self.create_publisher(PoseWithCovarianceStamped, '/sensing/gnss/pose_with_covariance', 10)
        self.timer = self.create_timer(1.0, self.publish_pose)

    def publish_pose(self):
        pose_msg = PoseWithCovarianceStamped()
        pose_msg.header = Header()
        pose_msg.header.stamp = self.get_clock().now().to_msg()
        pose_msg.header.frame_id = 'map'
        pose_msg.pose.pose.position.x = 0.0
        pose_msg.pose.pose.position.y = 0.0
        pose_msg.pose.pose.position.z = 0.0
        pose_msg.pose.pose.orientation.x = 0.0
        pose_msg.pose.pose.orientation.y = 0.0
        pose_msg.pose.pose.orientation.z = 0.0
        pose_msg.pose.pose.orientation.w = 1.0

        covariance_matrix = [0.0] * 36  # 6x6 covariance matrix
        pose_msg.pose.covariance = covariance_matrix

        self.publisher.publish(pose_msg)
        self.get_logger().info('Published PoseWithCovarianceStamped message')

def main(args=None):
    rclpy.init(args=args)
    node = GNSSPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
