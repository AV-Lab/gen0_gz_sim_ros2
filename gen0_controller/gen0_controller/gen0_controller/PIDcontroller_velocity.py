#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Twist
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
        self.goal_point_path=Path()
        self.previous_goal_pose= Point()
        self.speed_msg= Twist()
        self.collisions= CollisionArray()
        self.state= 'nominal'
        self.vehicle_velocity = 0
        self.location_subscription = self.create_subscription(Odometry, '/localization/kinematic_state', self.path_velocity, 10)
        self.path_subscription = self.create_subscription(Path, '/planning/path', self.path_callback, 10)
        self.collisions_subscription = self.create_subscription(CollisionArray, '/controller/collisions', self.collisions_callback, 10)
        self.velocity_susbcription= self.create_subscription(VelocityReport, '/vehicle/status/velocity_status', self.velocity_callback, 10)
        self.publisher_speed= self.create_publisher(Twist, '/gen0_model/speed_cmd', 10)

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
                    if goal_pose != self.previous_goal_pose:
                        self.previous_goal_pose = goal_pose
                        self.velocities = self.generate_velocities(msg.pose.pose.position, goal_pose, 0)
                        # print("point to stop at: ", goal_pose)
                        # print("velocities: ", velocities)
                        # print("path to collision: ", self.goal_point_path)
                        print("*******************")
                        self.speed_msg.linear.x=self.velocity_pid.calculate(abs(self.velocities[-len(self.goal_point_path.poses)] - self.vehicle_velocity))
                        self.publisher_speed.publish(self.speed_msg)
        else:
            self.speed_msg.linear.x= 5.6
            self.publisher_speed.publish(self.speed_msg)

    def find_stop_point(self):
        # logic to find nearest collision
        nearest_collision_index=self.collisions.collisions[0].index
        for collision in self.collisions.collisions:
            if collision.index <= nearest_collision_index:
                nearest_collision_index= collision.index

        # logic to determine the goal point
        cumulative_distance= 0
        for i in range(nearest_collision_index, -1, -1):
            current_pose = self.path.poses[i-1].pose.position
            next_pose = self.path.poses[i].pose.position
            cumulative_distance += self.euclidean_distance(current_pose, next_pose)

            if cumulative_distance >= self.goal_pose_distance_threshold:
                # self.get_logger().info(f'Found pose at index {i} with cumulative distance: {cumulative_distance}')
                self.goal_point_path.poses = self.path.poses[:i]
                return current_pose
            
        self.get_logger().info(f'could not find a point less than 3m cumulative distance: {cumulative_distance}')
        return None
    
    # not complete
    def generate_velocities(self, vehicle_pose, goal_pose, s_speed):
        total_distance= sum(self.euclidean_distance(self.goal_point_path.poses[i].pose.position, self.goal_point_path.poses[i+1].pose.position) for i in range(len(self.goal_point_path.poses) - 1))
        total_speed_change= s_speed - self.vehicle_velocity
        velocities = [self.vehicle_velocity]
        current_distance = 0
        current_speed = self.vehicle_velocity
    
        for i in range(len(self.goal_point_path.poses) - 1):
            segment_distance = self.euclidean_distance(self.goal_point_path.poses[i].pose.position, self.goal_point_path.poses[i + 1].pose.position)
            current_distance += segment_distance
            
            # Calculate the new speed based on the proportion of the total distance covered
            current_speed = self.vehicle_velocity + (current_distance / total_distance) * total_speed_change
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

    def calculate(self, velocity_error):
        error = velocity_error 
        self.integral += error
        derivative = error - self.prev_error

        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        # print(output)

        self.prev_error = error
        return min(max(output, 0), 5.6)


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