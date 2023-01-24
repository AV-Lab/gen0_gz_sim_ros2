#!/usr/bin/env python3

import rospy
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Point
import sys
from visualization_msgs.msg import Marker, MarkerArray
import tf
import math


class PedestrianPoints:
    def __init__(self, names):
        self.data = None
        self.sub = rospy.Subscriber('gazebo/model_states', ModelStates, self.callback)
        self.marker_publisher = rospy.Publisher('visualization_markers', MarkerArray, queue_size=10)
        self.rate = rospy.Rate(10) # 1 Hz
        self.names= names
        self.counter=0
        self.markers = [MarkerArray() for size in range(len(names))]
        print(self.markers)
        self.points = [[[0 for col in range(3)] for row in range(2)] for depth in range(len(names))] # three dimensional list to store current position and previous position
        while not rospy.is_shutdown():
            self.getPosition()
            self.marker_publisher.publish(self.markers[0])
            self.rate.sleep()

    def callback(self,data):
        self.data = data

    def getPosition(self):
        if self.data:
            try:
                idx_car = self.data.name.index("catvehicle")
                position_car = self.data.pose[idx_car].position
                for p in range(0, len(self.names)):
                    idx_actor = self.data.name.index(self.names[p]) # Get the ID of pedestrian in gazebo
                    position_actor = self.data.pose[idx_actor].position
                    self.publishMarker(p, position_actor.x - position_car.x, position_actor.y - position_car.y, position_actor.z - position_car.z)
                    # print("{} position: x={}, y={}, z={}".format(self.names[p], position_actor.x, position_actor.y, position_actor.z))
                    # print("car position: x={}, y={}, z={}".format(position_car.x, position_car.y, position_car.z))
                    # print("relative position: x={}, y={}, z={}".format(position_actor.x - position_car.x, position_actor.y - position_car.y, position_actor.z - position_car.z))
            except ValueError:
                print("Model not found")
        else:
            print("Data not received yet.")

    def publishMarker(self, index, x, y, z):
        self.points[index][1]= self.points[index][0] # previous points will become current
        self.points[index][0]= [x, y, z] # new points
        angle = math.atan2(y- self.points[index][1][1], x - self.points[index][1][0])

        marker = Marker()
        marker.header.frame_id = "catvehicle/base_link"
        marker.type = marker.ARROW
        marker.action = marker.ADD
        marker.scale.x = 0.25
        marker.scale.y = 0.05
        marker.scale.z = 0.05
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        quat = tf.transformations.quaternion_from_euler(0, 0, angle)
        marker.pose.orientation.x = quat[0]
        marker.pose.orientation.y = quat[1]

        marker.pose.orientation.z = quat[2]
        marker.pose.orientation.w = quat[3]
        marker.pose.position.x = x
        marker.pose.position.y = y
        marker.pose.position.z = z

        marker.id = len(self.markers[index].markers)
        print(marker.id)
        self.markers[index].markers.append(marker)
        if len(self.markers[index].markers) == 16:
            self.markers[index].markers= []




if __name__ == '__main__':
    rospy.init_node('pedestrians_points')
    pedestrians_names= ["actor1"] # list of pedestirans names which can be taken from gazebo models
    PedestrianPoints(pedestrians_names)
