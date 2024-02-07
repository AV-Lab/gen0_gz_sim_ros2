#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from autoware_auto_planning_msgs.msg import Path, PathPoint
from geometry_msgs.msg import Pose, Quaternion
from tf_transformations import euler_from_quaternion

class PathSubscriber(Node):
    def __init__(self):
        super().__init__('path_subscriber')

        self.subscription = self.create_subscription(
            Path,
            '/planning/scenario_planning/lane_driving/behavior_planning/path',
            self.path_callback,
            10)
        
    def path_callback(self, msg):
        for path_point in msg.points:
            print([path_point.pose.position.x, path_point.pose.position.y, euler_from_quaternion([path_point.pose.orientation.x, path_point.pose.orientation.y, path_point.pose.orientation.z, path_point.pose.orientation.w])[2]],",")


def main(args=None):
    rclpy.init(args=args)
    node = PathSubscriber()
    try:
        rclpy.spin_once(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()