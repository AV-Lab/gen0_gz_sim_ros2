#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class DoorController(Node):
    def __init__(self):
        super().__init__('door_controller')

        self.right_forward_pub  = self.create_publisher(Float64, '/gen0_model/right_door/forward', 10)
        self.right_sideways_pub = self.create_publisher(Float64, '/gen0_model/right_door/sideways', 10)
        self.left_forward_pub   = self.create_publisher(Float64, '/gen0_model/left_door/forward', 10)
        self.left_sideways_pub  = self.create_publisher(Float64, '/gen0_model/left_door/sideways', 10)

        self.declare_parameter('action', 'open')
        self.action = self.get_parameter('action').get_parameter_value().string_value

        time.sleep(1.0)

        if self.action == 'open':
            self.open_doors()
        elif self.action == 'close':
            self.close_doors()
        else:
            self.get_logger().error("Invalid 'action' parameter. Use 'open' or 'close'.")

    def publish_float(self, pub, value: float):
        msg = Float64()
        msg.data = float(value)
        pub.publish(msg)

    def open_doors(self):
        self.get_logger().info('Opening doors...')

        self.publish_float(self.right_forward_pub, 0.08)
        self.publish_float(self.left_forward_pub, 0.08)
        time.sleep(2.0)

        self.publish_float(self.right_sideways_pub, 0.4)
        self.publish_float(self.left_sideways_pub, 0.4)
        
        self.get_logger().info('Doors opened successfully.')

    def close_doors(self):
        self.get_logger().info('Closing doors...')
    
        self.publish_float(self.right_sideways_pub, -0.4)
        self.publish_float(self.left_sideways_pub, -0.4)
        time.sleep(3.0)

        self.publish_float(self.right_forward_pub, -0.08)
        self.publish_float(self.left_forward_pub, -0.08)
        
        self.get_logger().info('Doors closed successfully.')


def main():
    rclpy.init()
    node = DoorController()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
