#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import xml.etree.ElementTree as ET
import sys
import os
from ament_index_python.packages import get_package_share_directory

class ActorsLoader(Node):
    def __init__(self):
        super().__init__('actors_loader')
        # initilze the parameters
        self.declare_parameter('actors_scenario', " ") # adding empty default just to remove the warning msg | the node is garanteed to have actors and world
        self.declare_parameter('world', " ")
        # get the parameters values from the launch file
        self.actors_scenario = self.get_parameter('actors_scenario').value 
        self.world = self.get_parameter('world').value
        self.package_directory= get_package_share_directory('gen0_main')
        self.add_scenario()

    def add_scenario(self):
        tree = ET.parse(self.package_directory + '/worlds/' + self.world + '/' + self.world + '.sdf')
        root = tree.getroot()
        world_element = root.find("world")
        if world_element is None:
            print("Error: No <world> element found in the base world file.")
            return
        for include in world_element.findall(".//include[@type='actors_scenario']"): # remove any existing scenarios
            world_element.remove(include)
        include_tag = ET.Element("include")
        include_tag.set("type", "actors_scenario") 
        uri_tag = ET.SubElement(include_tag, "uri")
        uri_tag.text = f"../worlds/scenarios/{self.world}/{self.actors_scenario}.sdf"  # Adjust this path as necessary

        world_element.append(include_tag)

        tree.write(self.package_directory + '/worlds/' + self.world + '/' + self.world + '.sdf')
    
def main(args=None):
    rclpy.init(args=args)
    node = ActorsLoader()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
