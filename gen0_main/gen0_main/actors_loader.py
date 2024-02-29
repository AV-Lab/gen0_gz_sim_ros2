#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import rclpy
from rclpy.node import Node
from ament_index_python.packages import get_package_share_directory

class ActorsLoader(Node):
    def __init__(self):
        super().__init__('actors_loader')
        self.declare_parameter('actors_scenario', " ")
        self.declare_parameter('world', " ")
        self.actors_scenario = self.get_parameter('actors_scenario').value 
        self.world = self.get_parameter('world').value
        self.package_directory = get_package_share_directory('gen0_main')
        self.add_scenario()

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
        actors_scenario_tree = ET.parse(actors_scenario_path)
        actors_scenario_root = actors_scenario_tree.getroot()

        # Assuming your actors are directly under the root in the actors_scenario.sdf
        for actor in actors_scenario_root.findall('actor'):
            actor_string = ET.tostring(actor, encoding='unicode')
            new_actor_element = ET.fromstring(actor_string)
            world_element.append(new_actor_element)

        # Write the modified world file back
        world_tree.write(world_file_path)

def main(args=None):
    rclpy.init(args=args)
    node = ActorsLoader()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


