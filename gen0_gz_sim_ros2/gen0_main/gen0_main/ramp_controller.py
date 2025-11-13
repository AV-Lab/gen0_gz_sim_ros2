#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class RampController(Node):
    def __init__(self):
        super().__init__('ramp_controller')

        self.ramp_forward_pub  = self.create_publisher(Float64, '/gen0_model/ramp/forward', 10)
        self.ramp_rotate_pub = self.create_publisher(Float64, '/gen0_model/ramp/rotate', 10)

        self.declare_parameter('action', 'open')
        self.action = self.get_parameter('action').get_parameter_value().string_value

        time.sleep(1.0)

        if self.action == 'open':
            self.open_ramp()
        elif self.action == 'close':
            self.close_ramp()
        else:
            self.get_logger().error("Invalid 'action' parameter. Use 'open' or 'close'.")

    def publish_float(self, pub, value: float):
        msg = Float64()
        msg.data = float(value)
        pub.publish(msg)

    def open_ramp(self):
        self.get_logger().info('Opening ramp...')

        self.publish_float(self.ramp_forward_pub, 1.48)
        time.sleep(4.0)

        self.publish_float(self.ramp_rotate_pub, -0.21)
        time.sleep(4.0)

        self.get_logger().info('Ramp opened successfully.')

    def close_ramp(self):
        self.get_logger().info('Closing ramp...')
        
        self.publish_float(self.ramp_rotate_pub, 0.21)
        time.sleep(3.0)

        self.publish_float(self.ramp_forward_pub, -1.48)
        time.sleep(2.0)

        self.get_logger().info('Ramp closed successfully.')


def main():
    rclpy.init()
    node = RampController()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
