#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from autoware_auto_control_msgs.msg import AckermannControlCommand, AckermannLateralCommand, LongitudinalCommand
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

class AckermannVehicle(Node):
    def __init__(self):
        super().__init__('ackermann_vehicle')
        self.subscription = self.create_subscription(
            AckermannControlCommand,
            '/control/command/control_cmd',
            self.cmd_callback,
            10
        )
        self.steering= Float64()
        self.speed= Twist()
        self.publisher_left = self.create_publisher(Float64, '/gen0_model/front_left_steering', 10)
        self.publisher_right = self.create_publisher(Float64, '/gen0_model/front_right_steering', 10)
        self.publisher_speed= self.create_publisher(Twist, '/gen0_model/speed_cmd', 10)
        self.logger = self.get_logger()
        
    def cmd_callback(self, msg):
        # self.logger.info(str(msg.lateral.steering_tire_angle))
        self.steering.data=msg.lateral.steering_tire_angle
        self.speed.linear.x=msg.longitudinal.speed
        self.publisher_left.publish(self.steering)
        self.publisher_right.publish(self.steering)
        self.publisher_speed.publish(self.speed)
        
def main(args=None):
    rclpy.init(args=args)
    node = AckermannVehicle()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()