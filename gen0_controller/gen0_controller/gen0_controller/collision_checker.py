#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import PoseArray
from gen0_controller_interfaces.msg import Collision, CollisionArray
import math

class CollisionChecker(Node):
    def __init__(self):
        super().__init__('collision_checker')
        self.subscription_path = self.create_subscription(Path, '/planning/path', self.path_callback, 10)
        self.subscription_odom = self.create_subscription(Odometry, '/localization/kinematic_state', self.odom_callback, 10)
        self.subscription_pedestrians = self.create_subscription(PoseArray, '/detection_pose_array', self.pedestrians_callback, 10)
        self.collision_publisher = self.create_publisher(CollisionArray, '/controller/collisions', 10)
        self.car_circles = []  # Car's detection circles
        self.path_circles = []  # Circles for the first N path points
        self.length = 1.99 # Car length
        self.width = 3.93 # Car width
        self.car_circle_radius = 2.0
        self.point_circle_radius = 2.0
        self.pedestrian_circle_radius = 1
        self.number_of_points = 15 # Lookahead distance

    def path_callback(self, msg):
        self.path_circles = [(pose.pose.position.x, pose.pose.position.y, pose.pose.position.z) for pose in msg.poses[:self.number_of_points]]

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        yaw = self.quaternion_to_yaw(msg.pose.pose.orientation)
        self.update_car_circles(x, y, yaw)

    def update_car_circles(self, x, y, yaw):
        offsets = [0, self.length/2, -self.length/2]  # Middle, front, and back positions
        self.car_circles = [(x + math.cos(yaw) * offset, y + math.sin(yaw) * offset) for offset in offsets]

    def pedestrians_callback(self, msg):
        all_collisions = CollisionArray()
        all_collisions.collisions = []
        all_collisions.state = "nominal"
        collision_detected = [False] * len(msg.poses)
        for i, pose in enumerate(msg.poses):
            px, py = pose.position.x, pose.position.y
            for car_circle in self.car_circles:
                if self.circles_intersect((px, py), self.pedestrian_circle_radius, car_circle, self.car_circle_radius):
                    collision_detected[i] = True
                    collision = Collision()
                    collision.pedestrian_position.x = px
                    collision.pedestrian_position.y = py
                    collision.global_path_point_position.x = car_circle[0]
                    collision.global_path_point_position.y = car_circle[1]
                    collision.collision_object_type = "car_circle"
                    all_collisions.collisions.append(collision)
                    all_collisions.state = "e_stop"
                    break

            if not collision_detected[i]:
                for path_circle in self.path_circles:
                    if self.circles_intersect((px, py), self.pedestrian_circle_radius, path_circle[:2], self.point_circle_radius):
                        collision_detected[i] = True
                        collision = Collision()
                        collision.pedestrian_position.x = px
                        collision.pedestrian_position.y = py
                        collision.global_path_point_position.x = path_circle[0]
                        collision.global_path_point_position.y = path_circle[1]
                        collision.collision_object_type = "global_path_point"
                        collision.index = path_circle[2] # index
                        all_collisions.collisions.append(collision)
                        if all_collisions.state != "e_stop":
                            all_collisions.state = "decelerate"
                        break

        self.collision_publisher.publish(all_collisions)

    def quaternion_to_yaw(self, quaternion):
        x, y, z, w = quaternion.x, quaternion.y, quaternion.z, quaternion.w
        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        return math.atan2(siny_cosp, cosy_cosp)

    def circles_intersect(self, center1, radius1, center2, radius2):
        distance = math.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
        return distance < (radius1 + radius2)

def main(args=None):
    rclpy.init(args=args)
    collision_checker = CollisionChecker()
    rclpy.spin(collision_checker)
    collision_checker.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
