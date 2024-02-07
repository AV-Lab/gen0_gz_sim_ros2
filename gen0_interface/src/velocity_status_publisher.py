#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from autoware_auto_vehicle_msgs.msg import VelocityReport

class VelocityStatusPublisher(Node):

    def __init__(self):
        super().__init__('velocity_status_publisher')
        self.publisher = self.create_publisher(VelocityReport, '/vehicle/status/velocity_status', 10)
        self.subscription = self.create_subscription(
            Odometry,
            '/gen0_model/odometry',
            self.velocity_callback,
            10)
        self.velocity_msg = VelocityReport()
        self.velocity_msg.longitudinal_velocity = 0.0
        self.velocity_msg.heading_rate= 0.0

    def velocity_callback(self, msg):

        linear_velocity= msg.twist.twist.linear.x

        self.velocity_msg.header.stamp = self.get_clock().now().to_msg()
        self.velocity_msg.header.frame_id = "base_link"

        if abs(linear_velocity) > 0.1:
            self.velocity_msg.longitudinal_velocity = linear_velocity
        else:
            self.velocity_msg.longitudinal_velocity = 0.0

        self.publisher.publish(self.velocity_msg)


def main(args=None):
    rclpy.init(args=args)
    node = VelocityStatusPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
