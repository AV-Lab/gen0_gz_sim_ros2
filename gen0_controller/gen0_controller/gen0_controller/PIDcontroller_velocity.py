#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Twist
from autoware_auto_vehicle_msgs.msg import VelocityReport
import math
from nav_msgs.msg import Odometry, Path
from gen0_controller_interfaces.msg import Collision, CollisionArray
from std_msgs.msg import Bool

class PIDControllerVelocityNode(Node):
    def __init__(self):
        super().__init__('pid_controller_velocity_node')
        self.goal_pose_distance_threshold = 3 + 1.5 # distance between the collision point and the stop point plus distance from the front to the center of the vehicle
        self.velocity_pid = PIDController(kp=3.0, ki=0.0, kd=1.0)
        self.path= Path()
        self.goal_point_path=Path()
        self.previous_goal_pose= Point()
        self.speed_msg= Twist()
        self.collisions= CollisionArray()
        self.state= 0
        self.vehicle_velocity = 0.0
        self.location_subscription = self.create_subscription(Odometry, '/localization/kinematic_state', self.path_velocity, 10)
        self.path_subscription = self.create_subscription(Path, '/planning/path', self.path_callback, 10)
        self.collisions_subscription = self.create_subscription(CollisionArray, '/controller/collisions', self.collisions_callback, 10)
        self.velocity_susbcription= self.create_subscription(VelocityReport, '/vehicle/status/velocity_status', self.velocity_callback, 10)
        self.publisher_speed= self.create_publisher(Twist, '/gen0_model/speed_cmd', 10)
        self.subscription = self.create_subscription(Bool, '/planning/green_signal', self.signal_callback, 10)
        self.proceed= False
        self.deceleration= 1.5 # limitation by the real vehicle
        self.estop_deceleration= 6.25 # assuming a full brake and based on the stopping distance equation
        self.persistent = False

    def path_velocity(self, msg):
        if self.collisions.collisions:
            self.state=0
            if self.collisions.state == 'e_stop':
                self.speed_msg.linear.x= 0.0
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
                        print("*******************")

                    # print("velocities are: ", self.velocities)
                    # print(self.goal_point_path.poses)
                    self.speed_msg.linear.x=self.velocities[-(len(self.goal_point_path.poses))]
                    # print(self.velocities[-(len(self.goal_point_path.poses))])
                else:
                    self.speed_msg.linear.x= 0.0
                    print("failed to decelerate in time, to estop")
                self.publisher_speed.publish(self.speed_msg) 
        else:
            if self.state != 1:
                print("No collisions")
                self.previous_goal_pose = None # very important to reset the previous_goal_pose if there are no more collisions
                self.state = 1
            # make sure there is a path
            if self.path.poses:
                if self.path.poses[0].pose.orientation.x == 1.0:
                    self.speed_msg.linear.x = 0.0
                    while self.vehicle_velocity != 0.0 and self.persistent: # dont allow the vehicle to proceed until the vehicle is completely stopped
                        self.proceed = False
                        self.persistent= False
                        self.publisher_speed.publish(self.speed_msg)
                if self.proceed:
                    if self.path.poses[1]: # check if a new path has been loaded, or the current path still have points
                        if self.path.poses[0].pose.orientation.x == 1.0: # if there is a stop flag in the current waypoint, find the velocity of the next one
                            self.speed_msg.linear.x= self.path.poses[1].pose.orientation.y # velocity element from path, check PIDcontroller_CTE publish_path()
                        else:
                            self.persistent= True # reset the persistent flag
                            self.speed_msg.linear.x= self.path.poses[0].pose.orientation.y
                    else: # write 0.3 speed until a new path arrives
                        self.speed_msg.linear.x= 0.3  # use the velocity of 0.3 to begin with
                else:
                    self.speed_msg.linear.x = 0.0
                self.publisher_speed.publish(self.speed_msg)
            else:
                print("waiting to receive path")

    def find_stop_point(self):
        # logic to find nearest collision
        nearest_collision_index=self.collisions.collisions[0].index
        for collision in self.collisions.collisions:
            if collision.index <= nearest_collision_index:
                nearest_collision_index= collision.index

        # logic to determine the goal point
        cumulative_distance= 0
        global_path = self.path.poses # assigning the current global path to a variable to avoid the affect path changes during the execution of the for loop

        for i in range(int(nearest_collision_index) - int(global_path[0].pose.position.z), 0, -1):
            current_pose = global_path[i-1].pose.position
            next_pose = global_path[i].pose.position
            cumulative_distance += self.euclidean_distance(current_pose, next_pose)

            if cumulative_distance >= self.goal_pose_distance_threshold:
                self.get_logger().info(f'Found pose at index {i} with cumulative distance: {cumulative_distance}')
                self.goal_point_path.poses = global_path[:i]
                return current_pose
            
        self.get_logger().info(f'could not find a point less than {self.goal_pose_distance_threshold} cumulative distance: {cumulative_distance}')
        return None
    
    # not complete
    def generate_velocities(self, vehicle_pose, goal_pose, s_speed):
        distances = []
        velocities = [self.vehicle_velocity]

        for i in range(len(self.goal_point_path.poses) - 1):
            distances.append(self.euclidean_distance(self.goal_point_path.poses[i].pose.position, self.goal_point_path.poses[i+1].pose.position))
            previous_speed = velocities[-1]
            distance = distances[i]
            # make sure the speed is not negative
            try:
                new_speed = math.sqrt(previous_speed**2 - 2 * self.deceleration * distance)
            except ValueError: 
                new_speed = 0.0
            velocities.append(new_speed)
    
        return velocities
        

    def euclidean_distance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

    def path_callback(self, msg):
        self.path=msg

    def collisions_callback(self, msg):
        self.collisions= msg
    
    def velocity_callback(self, msg):
        self.vehicle_velocity= msg.longitudinal_velocity
    
    def signal_callback(self, msg):
        self.proceed = msg.data


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