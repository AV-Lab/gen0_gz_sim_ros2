#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion
import time

class LocalizationPoints(Node):
    def __init__(self):
        super().__init__('localization_points')

        self.localization_points=[]

        self.subscription = self.create_subscription(
            Odometry, 
            '/localization/kinematic_state',
            self.points_callback,
            10)
        
    def points_callback(self, msg):
        self.localization_points.append([msg.pose.pose.position.x, msg.pose.pose.position.y, euler_from_quaternion([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])[2]])


def main(args=None):
    rclpy.init(args=args)
    node = LocalizationPoints()
    while True:
        try:
            rclpy.spin_once(node)
            time.sleep(1)
        except KeyboardInterrupt:
            for i in range(len(node.localization_points)):
                print(node.localization_points[i],",")
            node.destroy_node()
            rclpy.shutdown()

if __name__ == '__main__':
    main()
