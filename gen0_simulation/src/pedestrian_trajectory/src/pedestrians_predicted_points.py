#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseArray
from visualization_msgs.msg import Marker, MarkerArray
from copy import deepcopy

class PedestrianPredictedPoints:
    def __init__(self):
        self.marker=Marker()
        self.markerarray=MarkerArray()
        self.pedestrian_subscriber = rospy.Subscriber('pedestrian_predicted_position', PoseArray, self.callback)
        self.marker_publisher = rospy.Publisher('visualization_markers', MarkerArray, queue_size=10)

    def callback(self, data):
        counter=0
        for pose in (data.poses):
            counter=counter + 1
            self.marker.header.frame_id = "catvehicle/base_link"
            self.marker.type = self.marker.SPHERE
            self.marker.action = self.marker.ADD
            self.marker.scale.x = 0.1
            self.marker.scale.y = 0.1
            self.marker.scale.z = 0.1
            self.marker.color.a = 1.0
            self.marker.color.r = 0.0
            self.marker.color.g = 0.0
            self.marker.color.b = 1.0
            self.marker.pose=pose
            self.marker.id = counter
            self.markerarray.markers.append(deepcopy(self.marker))
        # print(self.markerarray)
        self.marker_publisher.publish(self.markerarray)
        self.markerarray= MarkerArray()

if __name__ == '__main__':
    rospy.init_node('pedestrians_predicted_points')
    PedestrianPredictedPoints()
    rospy.spin()
