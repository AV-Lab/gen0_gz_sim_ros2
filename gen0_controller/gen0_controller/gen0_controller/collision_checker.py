#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path, Odometry
from geometry_msgs.msg import PoseArray
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import matplotlib.transforms as transforms
import math
import matplotlib

matplotlib.style.use('seaborn-darkgrid')

class CollisionCheck(Node):
    def __init__(self):
        super().__init__('collision_checker')
        self.subscription_path = self.create_subscription(Path, '/planning/path', self.path_callback, 10)
        self.subscription_odom = self.create_subscription(Odometry, '/localization/kinematic_state', self.odom_callback, 10)
        self.subscription_pedestrians = self.create_subscription(PoseArray, '/actors/poses', self.pedestrians_callback, 10)
        self.car = None  # This will hold the rectangle representing the car
        self.car_circles = []  # Car's detection circles
        self.path_circles = []  # Circles for the first N path points
        self.pedestrian_circles = []  # Circles for pedestrians
        self.length = 1.99
        self.width = 3.93
        self.car_circle_radius = 2.0
        self.point_circle_radius = 1.5
        self.pedestrian_circle_radius = 1
        self.plot_range_x = 50
        self.plot_range_y = 50
        self.number_of_points = 30
        self.initialize_plot()

    def initialize_plot(self):
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.line_all, = self.ax.plot([], [], 'o-', color='blue')
        self.line_topN, = self.ax.plot([], [], 'o-', color='blue')
        self.ax.legend(loc='upper left', frameon=True)
        plt.title('Live Path and Car Position Update')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.legend()
        plt.grid(True)
        # Initialize circles for the car
        for _ in range(3):
            circle = Circle((0, 0), self.car_circle_radius, color='green', fill=False)
            self.ax.add_patch(circle)
            self.car_circles.append(circle)

    def path_callback(self, msg):
        x_all = [pose.pose.position.x for pose in msg.poses]
        y_all = [pose.pose.position.y for pose in msg.poses]
        x_topN = x_all[:self.number_of_points]
        y_topN = y_all[:self.number_of_points]
        self.update_plot(x_all, y_all, x_topN, y_topN)
        # Draw/update circles for the detection points
        for i, pose in enumerate(msg.poses[:self.number_of_points]):
            if i >= len(self.path_circles):
                # Create new circle if not enough exist
                circle = Circle((pose.pose.position.x, pose.pose.position.y), self.point_circle_radius, color='green', fill=False)
                # self.ax.add_patch(circle)
                self.path_circles.append(circle)
            else:
                # Update position of existing circle
                self.path_circles[i].center = (pose.pose.position.x, pose.pose.position.y)


    def update_plot(self, x_all, y_all, x_topN, y_topN):
        self.line_all.set_data(x_all, y_all)
        self.line_topN.set_data(x_topN, y_topN)
        self.ax.relim()
        self.ax.autoscale_view()

    def odom_callback(self, msg):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        yaw = self.quaternion_to_yaw(msg.pose.pose.orientation)
        if not self.car:
            self.car = Rectangle((x - self.width/2, y - self.length/2), self.width, self.length, color='black', label='Car', fill=False)
            self.ax.add_patch(self.car)
        else:
            self.car.set_xy((x - self.width/2, y - self.length/2))
            rotation = transforms.Affine2D().rotate_around(x, y, yaw) + self.ax.transData
            self.car.set_transform(rotation)
        self.update_car_circles(x, y, yaw)
        self.ax.set_xlim(x - self.plot_range_x / 2, x + self.plot_range_x / 2)
        self.ax.set_ylim(y - self.plot_range_y / 2, y + self.plot_range_y / 2)

    def update_car_circles(self, x, y, yaw):
        offsets = [0, self.length/2, -self.length/2]  # Middle, front, and back positions
        for offset, circle in zip(offsets, self.car_circles):
            offset_x = math.cos(yaw) * offset
            offset_y = math.sin(yaw) * offset
            circle.center = (x + offset_x, y + offset_y)

    def pedestrians_callback(self, msg):
        collision_detected = [False] * len(msg.poses)
        for i, pose in enumerate(msg.poses):
            if i >= len(self.pedestrian_circles):
                circle = Circle((pose.position.x, pose.position.y), self.pedestrian_circle_radius, color='yellow', fill=False)
                self.ax.add_patch(circle)
                self.pedestrian_circles.append(circle)
            else:
                self.pedestrian_circles[i].center = (pose.position.x, pose.position.y)
            
            # Check collisions with car circles
            for car_circle in self.car_circles:
                if self.circles_intersect((pose.position.x, pose.position.y), self.pedestrian_circle_radius, car_circle.center, car_circle.radius):
                    collision_detected[i] = True
                    break

            # Check collisions with path circles if no collision detected yet
            if not collision_detected[i]:
                for path_circle in self.path_circles:
                    if self.circles_intersect((pose.position.x, pose.position.y), self.pedestrian_circle_radius, path_circle.center, path_circle.radius):
                        collision_detected[i] = True
                        break

            # Update circle color based on collision
            self.pedestrian_circles[i].set_color('red' if collision_detected[i] else 'orange')

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def quaternion_to_yaw(self, quaternion):
        x, y, z, w = quaternion.x, quaternion.y, quaternion.z, quaternion.w
        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)
        return yaw
    
    def circles_intersect(self, center1, radius1, center2, radius2):
        distance = math.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
        return distance < (radius1 + radius2)

def main(args=None):
    rclpy.init(args=args)
    collision_checker = CollisionCheck()
    rclpy.spin(collision_checker)
    collision_checker.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
