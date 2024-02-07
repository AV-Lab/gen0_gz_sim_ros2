#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math
from nav_msgs.msg import Odometry
from collections import deque
from tf_transformations import euler_from_quaternion
from autoware_auto_control_msgs.msg import AckermannControlCommand
from gen0_controller_interfaces.srv import PathLoad
from gen0_controller_interfaces.msg import PathPoints
import numpy as np

class PIDControllerCTENode(Node):
    def __init__(self):
        super().__init__('pid_controller_cte_node')

        # Initialize PID parameters for steering and speed control
        self.steering_pid = PIDController(kp=3.0, ki=0.0, kd=1.0)
        self.starting_point= True

        self.path_client = self.create_client(PathLoad, 'get_path')
        while not self.path_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warning('Waiting for PathLoader')
        self.request = PathLoad.Request()

        self.path=deque()
        self.waiting_for_service=False

        self.control_cmd= AckermannControlCommand()

        self.control_publisher = self.create_publisher(
            AckermannControlCommand,
            '/control/command/control_cmd',
            10
        )
        
        self.subscription = self.create_subscription(Odometry, '/localization/kinematic_state',self.path_tracking, 10)

    def path_tracking(self, msg):
        if (not self.path or len(self.path) <= 1) and not self.waiting_for_service:
            self.get_logger().warning('Waiting for path to be loaded')
            try:
                self.future = self.path_client.call_async(self.request) 
                print("Service called")           
                self.waiting_for_service= True  
            except Exception as e:
                self.get_logger().error(f'Service call exception: {str(e)}')
            return
        elif self.waiting_for_service:
            self.path.extend(self.path_loader())
            return
    
        # Current position in (x,y,yaw) format
        vehicle_position= [msg.pose.pose.position.x, msg.pose.pose.position.y, euler_from_quaternion([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])[2]]

        # Find the next goal based on the closest distance
        try:
            target_position, future_position = self.find_target_pose(vehicle_position)
        except: # Not a good way but lazy way to prevent the race condition from killing the code
            return

        cross_track_error= self.find_cross_track_error(vehicle_position[:2], target_position[:2], future_position[:2])
        # Calculate steering based on CTE
        steering_command = self.steering_pid.calculate(cross_track_error)

        self.control_cmd.lateral.steering_tire_angle=steering_command
        self.control_cmd.longitudinal.speed=3.0
        # Publish control commands
        self.control_publisher.publish(self.control_cmd)
    
    def find_target_pose(self, vehicle_position):
        current_goal_distance = math.sqrt((self.path[0][0] - vehicle_position[0]) ** 2 + (self.path[0][1] - vehicle_position[1]) ** 2)
        next_goal_distance = math.sqrt((self.path[1][0] - vehicle_position[0]) ** 2 + (self.path[1][1] - vehicle_position[1]) ** 2)
        if next_goal_distance < current_goal_distance:
            self.get_logger().debug('Updating goal point....')
            self.path.popleft()
        if len(self.path) > 1:
            target_pose = self.path[0] 
            future_position= self.path[1]
            return target_pose, future_position
        else:
            self.path.popleft()
            self.get_logger().info('Path Completed')
            self.control_cmd.longitudinal.speed=0.0
            self.control_cmd.lateral.steering_tire_angle=0.0
            self.control_publisher.publish(self.control_cmd)

    def find_cross_track_error(self, vehicle_position, target_position, future_position):
        path_vector= np.array([future_position[0] - target_position[0], future_position[1] - target_position[1]]) # vector from target position to future position
        vehicle_vector=np.array([vehicle_position[0] - target_position[0], vehicle_position[1] - target_position[1]]) # vector from target position to vehicle position
        path_vector_normalized= self.normalize_vector(path_vector) # normalize the path_vector to be used to compute projection 
        vehicle_path_vector= np.dot(vehicle_vector, path_vector_normalized) * path_vector_normalized # project the vehicle_vector onto path_vector
        cross_track_error = np.linalg.norm(vehicle_vector - vehicle_path_vector) # subtract the vehicle_vector from vehicle_path_vector then find the magnitude to determine the distance

        cross_product = (path_vector[0] * vehicle_vector[1]) - (path_vector[1] * vehicle_vector[0])
        cross_track_error= math.copysign(cross_track_error, cross_product) # the sign of the cross product determines the steering direction

        return -1 * cross_track_error
    
    def normalize_vector(self, vector):
        magnitude = np.linalg.norm(vector)
        if magnitude == 0:
            return vector
        return vector / magnitude
    
    def path_loader(self):
        path=[]
        if self.future.done():
            self.waiting_for_service=False
            print("Service Completed")
            if self.future.result() is not None:
                response = self.future.result()
                for point in response.path:
                    path.append(point.point)
                path = [point.tolist() for point in path]
                self.get_logger().info('Path Received')
            else:
                self.get_logger().error('Service call failed')
        return path

    def destroy(self):
        super().destroy_node()
        rclpy.shutdown()

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
        return min(max(output, -0.6), 0.6)

def main(args=None):
    rclpy.init(args=args)
    node = PIDControllerCTENode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
