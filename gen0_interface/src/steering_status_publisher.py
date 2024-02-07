#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from autoware_auto_vehicle_msgs.msg import SteeringReport

class SteeringStatusPublisher(Node):

    def __init__(self):
        super().__init__('steering_status_publisher')
        self.publisher = self.create_publisher(SteeringReport, '/vehicle/status/steering_status', 10)
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_states_callback,
            10
        )
        self.steering_msg = SteeringReport()
        self.steering_msg.steering_tire_angle = 0.0

    def joint_states_callback(self, msg):
        # Find the index of the 'front_right_steering_joint' in the joint names list
        joint_name = 'front_right_steering_joint'
        if joint_name in msg.name:
            index = msg.name.index(joint_name)
            # Get the joint position from the message
            joint_position = msg.position[index]
            # Apply the condition to publish non-zero values
            if abs(joint_position) > 0.1:
                self.steering_msg.steering_tire_angle = joint_position
            else:
                self.steering_msg.steering_tire_angle = 0.0

            self.steering_msg.stamp = self.get_clock().now().to_msg()
            # Publish the updated steering status
            self.publisher.publish(self.steering_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SteeringStatusPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
