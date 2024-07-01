#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from pynput import keyboard
from autoware_auto_control_msgs.msg import AckermannControlCommand # Replace with your actual message type

class TeleopNode(Node):
    def __init__(self):
        super().__init__('keyboard_teleop')
        self.publisher_ = self.create_publisher(AckermannControlCommand, '/gen0_model/command/control_cmd', 10)
        self.control_cmd = AckermannControlCommand()
        self.control_cmd.lateral.steering_tire_angle=0.0
        self.control_cmd.longitudinal.speed = 0.0

        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

        self.get_logger().info("Keyboard teleop started. Use 'WASD' keys to control the robot. Press 'R' to reset steering angle to 0. Press 'Esc' to exit.")

    def on_press(self, key):
        try:
            if key.char == 'w':
                self.control_cmd.longitudinal.speed = min(self.control_cmd.longitudinal.speed + 0.1, 5.0)
            elif key.char == 's':
                self.control_cmd.longitudinal.speed = max(self.control_cmd.longitudinal.speed - 0.1, 0.0)
            elif key.char == 'a':
                self.control_cmd.lateral.steering_tire_angle = min(self.control_cmd.lateral.steering_tire_angle + 0.1, 0.5)
            elif key.char == 'd':
                self.control_cmd.lateral.steering_tire_angle = max(self.control_cmd.lateral.steering_tire_angle - 0.1, -0.5)
            elif key.char == 'r':
                self.control_cmd.lateral.steering_tire_angle = 0.0
        except AttributeError:
            pass

        self.publisher_.publish(self.control_cmd)

    def on_release(self, key):
        if key == keyboard.Key.esc:
            # Stop listener
            return False

def main(args=None):
    rclpy.init(args=args)
    teleop_node = TeleopNode()

    try:
        rclpy.spin(teleop_node)
    except KeyboardInterrupt:
        pass
    finally:
        teleop_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
