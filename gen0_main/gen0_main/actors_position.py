#!/usr/bin/env python3


import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Time
from rosgraph_msgs.msg import Clock
import xml.etree.ElementTree as ET
import numpy as np
from ament_index_python.packages import get_package_share_directory


class ActorPositionTracker(Node):
    def __init__(self):
        super().__init__('actor_position_tracker')
        self.get_logger().info("node started")
        self.package_directory = get_package_share_directory('gen0_main')
        self.subscription = self.create_subscription(
            Clock,
            '/clock',
            self.clock_callback,
            10)
        self.subscription  # prevent unused variable warning

        # Load and parse the SDF file
        self.tree = ET.parse(self.package_directory + '/worlds/' + 'san_roundabout' + '/' + 'san_roundabout' + '.sdf')  # Update this path
        self.root = self.tree.getroot()
        

    def interpolate_position(self, time, waypoints):
        # Calculate the maximum time from the waypoints
        max_time = waypoints[-1][0]
        # Adjust time for looping if it exceeds the maximum time in the waypoints
        if time > max_time:
            time = time % max_time

        before = waypoints[0]
        after = waypoints[-1]
        for waypoint in waypoints:
            if time < waypoint[0]:
                after = waypoint
                break
            before = waypoint

        # Linear interpolation between the before and after waypoints
        t1, pos1 = before
        t2, pos2 = after
        t_ratio = (time - t1) / (t2 - t1) if t2 != t1 else 0
        interpolated_pos = pos1 + t_ratio * (pos2 - pos1)
        return interpolated_pos

    def get_actor_positions(self, time):
        actors = self.root.findall(".//actor")
        actor_positions = {}
        for actor in actors:
            name = actor.get('name')
            waypoints = []
            for waypoint in actor.findall(".//waypoint"):
                t = float(waypoint.find('time').text)
                pose = np.array(list(map(float, waypoint.find('pose').text.split())))
                waypoints.append((t, pose[:3]))  # Only take x, y, z for position
            interpolated_pos = self.interpolate_position(time, waypoints)
            actor_positions[name] = interpolated_pos
        return actor_positions

    def clock_callback(self, msg):
        simulation_time = msg.clock.sec + msg.clock.nanosec * 1e-9
        actor_positions = self.get_actor_positions(simulation_time)
        position = actor_positions.get("pedestrian_1")
        self.get_logger().info(f"Actor: pedestrian_1 Interpolated Position: {position}")
        # for actor, position in actor_positions.items():
        #     self.get_logger().info(f"Actor: {actor}, Interpolated Position: {position}")

def main(args=None):
    rclpy.init(args=args)
    actor_position_tracker = ActorPositionTracker()
    rclpy.spin(actor_position_tracker)
    actor_position_tracker.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
