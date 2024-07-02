#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory
import os
import tf2_ros
from geometry_msgs.msg import PoseArray, PoseStamped
import tf2_geometry_msgs

class ActorsLoader(Node):
    def __init__(self):
        super().__init__('actors_loader')
        self.declare_parameter('actors_scenario', " ")
        self.declare_parameter('world', " ")
        self.actors_scenario = self.get_parameter('actors_scenario').value 
        self.world = self.get_parameter('world').value
        self.package_directory = get_package_share_directory('gen0_main')
        self.actor_topics = [] # List of all topics of actors for poses
        self.actors_subscriptions = [] # List of all subscriptions to actors
        self.actor_positions = {}  # Dictionary to store latest positions of actors
        self.publisher = self.create_publisher(PoseArray, '/actors/poses', 10)
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        # wait for transform world -> map to appear
        while not self.tf_buffer.can_transform('lanelet_map', 'world', rclpy.time.Time().to_msg()):
            self.get_logger().info("Waiting for transform...")
            rclpy.spin_once(self)  # Spin once to process events

        self.add_scenario()
        self.subscribe_to_actors()

    def add_scenario(self):
        # Load the world file
        world_file_path = self.package_directory + '/worlds/' + self.world + '/' + self.world + '.sdf'
        world_tree = ET.parse(world_file_path)
        world_root = world_tree.getroot()
        world_element = world_root.find("world")

        if world_element is None:
            print("Error: No <world> element found in the base world file.")
            return
        
        # Remove existing actors
        actors = world_element.findall('actor')
        for actor in actors:
            world_element.remove(actor)
        
        # Load the actors scenario file
        actors_scenario_path = self.package_directory + '/worlds/scenarios/' + self.world + '/' + self.actors_scenario + '.sdf'
        if os.path.exists(actors_scenario_path):
            actors_scenario_tree = ET.parse(actors_scenario_path)
            actors_scenario_root = actors_scenario_tree.getroot()

            # Assuming your actors are directly under the root in the actors_scenario.sdf
            for actor in actors_scenario_root.findall('actor'):
                actor_string = ET.tostring(actor, encoding='unicode')
                new_actor_element = ET.fromstring(actor_string)
                world_element.append(new_actor_element)
                self.actor_topics.append("/actor/" + actor.get('name') + "/pose") 

        # Write the modified world file back
        world_tree.write(world_file_path)

    def subscribe_to_actors(self):
        self.get_logger().info("Available actor topics: " + str(self.actor_topics))
        for topic in self.actor_topics:
            subscription = self.create_subscription(
                PoseStamped,
                topic,
                lambda msg, actor_name=topic[1:]: self.actor_position_callback(msg, actor_name),
                10)
            self.actors_subscriptions.append(subscription)
    
    def actor_position_callback(self, msg, actor_name):
        msg.header.frame_id= 'world' # manually setting the frame id, as the publisher is coming from gz-ros bridge and it does not have a frame id
        msg_transformed= self.tf_buffer.transform(msg, 'lanelet_map') # transform from world position to map
        self.actor_positions[actor_name] = msg_transformed
        pose_array_msg = PoseArray()
        pose_array_msg.header.stamp=self.get_clock().now().to_msg()

        for actor_name, position in self.actor_positions.items():
            pose_array_msg.poses.append(position.pose)
        
        self.publisher.publish(pose_array_msg)


def main(args=None):
    rclpy.init(args=args)
    node = ActorsLoader()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


