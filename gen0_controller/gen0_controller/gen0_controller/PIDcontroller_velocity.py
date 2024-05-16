#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import  Point
from autoware_auto_vehicle_msgs.msg import VelocityReport
import math
from nav_msgs.msg import Odometry, Path
from gen0_controller_interfaces.msg import Collision, CollisionArray

class PIDControllerVelocityNode(Node):
    def __init__(self):
        super().__init__('pid_controller_velocity_node')
        self.n_points= 50 # number of points for linear interporlation
        self.goal_pose_distance_threshold = 3 # distance between the collision point and the stop point
        self.velocity_pid = PIDController(kp=3.0, ki=0.0, kd=1.0)
        self.path= Path()
        self.collisions= CollisionArray()
        self.state= 'nominal'
        self.vehicle_velocity = 0
        self.location_subscription = self.create_subscription(Odometry, '/localization/kinematic_state', self.path_velocity, 10)
        self.path_subscription = self.create_subscription(Path, '/planning/path', self.path_callback, 10)
        self.collisions_subscription = self.create_subscription(CollisionArray, '/controller/collisions', self.collisions_callback, 10)
        self.velocity_susbcription= self.create_subscription(VelocityReport, '/vehicle/status/velocity_status', self.velocity_callback, 10)

    def path_velocity(self, msg):
        if self.collisions.collisions:
            if self.collisions.state == 'e_stop':
                print('e_stop')
                # Need to implement emergency break here #
                #                                        #
                #                                        #
                pass
            else:
                goal_pose=self.find_stop_point()
                if goal_pose:
                    self.generate_velocities(msg.pose.pose.position, goal_pose, 0)
        else:
            pass
            # Nominal state

    def find_stop_point(self):
        # logic to find nearest collision
        nearest_collision_index=0
        collision_point= Point()
        for collision in self.collisions.collisions:
            if collision.index >= nearest_collision_index:
                nearest_collision_index= collision.index
                collision_point= collision.global_path_point_position
        # logic to determine the goal point
        cumulative_distance= 0
        for i in range(nearest_collision_index-1, -1, -1):
            current_pose = self.path.poses[i].pose.position
            next_pose = self.path.poses[i+1].pose.position if i < nearest_collision_index-1 else collision_point
            cumulative_distance += self.euclidean_distance(current_pose, next_pose)

            if cumulative_distance >= self.goal_pose_distance_threshold:
                self.get_logger().info(f'Found pose at index {i} with cumulative distance: {cumulative_distance}')
                return current_pose
            
        self.get_logger().info(f'could not find a point less than 3m cumulative distance: {cumulative_distance}')
        return None
    
    def generate_velocities(self, vehicle_pose, goal_pose, s_speed):
        velocities = []
        speed_increment = (s_speed - self.vehicle_velocity) / (self.n_points - 1)
    
        for i in range(self.n_points):
            current_speed = self.vehicle_velocity + i * speed_increment
            velocities.append(current_speed)
    
        return velocities
        

    def euclidean_distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

    def path_callback(self, msg):
        self.path=msg

    def collisions_callback(self, msg):
        self.collisions= msg
    
    def velocity_callback(self, msg):
        self.vehicle_velocity= msg.longitudinal_velocity


class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def calculate(self, cross_track_error):
        error = cross_track_error 
        self.integral += error
        derivative = error - self.prev_error

        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        # print(output)

        self.prev_error = error
        return min(max(output, 0), 2)


def main(args=None):
    rclpy.init(args=args)
    node = PIDControllerVelocityNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy()
    rclpy.shutdown()

if __name__ == '__main__':
    main()