#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from gen0_controller_interfaces.srv import PathLoad
from gen0_controller_interfaces.msg import PathPoints
import json
import os
import time

class PathService(Node):

    def __init__(self):
        super().__init__('path_service')
        self.path_service = self.create_service(PathLoad, 'get_path', self.handle_get_path)
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.next_station='station1.json'

    def handle_get_path(self, request, response):
        # time.sleep(10)
        self.file_path = os.path.join(self.script_dir, '..', '..', 'share', 'gen0_controller', 'stations', self.next_station)
        print(self.next_station)
        try:
            with open(self.file_path, 'r') as file:
                path_data = json.load(file)
        except FileNotFoundError:
            self.get_logger().error('Path file not found')
            return response

        # Convert the path data to PathPoints.msg format
        response.path = [PathPoints(point=point) for point in path_data]

        if self.next_station == 'station1.json':
            self.next_station='station2.json'
        else:
            self.next_station='station1.json'
        return response

def main(args=None):
    rclpy.init(args=args)
    path_service = PathService()
    rclpy.spin(path_service)
    path_service.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
