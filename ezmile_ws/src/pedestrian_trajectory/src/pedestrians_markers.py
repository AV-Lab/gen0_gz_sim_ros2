#!/usr/bin/env python3

import rospy
from visualization_msgs.msg import Marker, MarkerArray
import tf

class PedestrianMarkers:
    def __init__(self):
        self.pedestrian_subscriber = rospy.Subscriber('visualization_markers', MarkerArray, queue_size=10)
        self.marker_publisher = rospy.Publisher('visualization_markers', MarkerArray, queue_size=10)
        self.markers = MarkerArray()

        marker1 = Marker()
        marker1.header.frame_id = "catvehicle/base_link"
        marker1.type = marker1.ARROW
        marker1.action = marker1.ADD
        marker1.scale.x = 0.25
        marker1.scale.y = 0.05
        marker1.scale.z = 0.05
        marker1.color.a = 1.0
        marker1.color.r = 1.0
        marker1.color.g = 0.0
        marker1.color.b = 0.0
        quat = tf.transformations.quaternion_from_euler(0, 0, 3.1415926535)
        marker1.pose.orientation.x = quat[0]
        marker1.pose.orientation.y = quat[1]
        marker1.pose.orientation.z = quat[2]
        marker1.pose.orientation.w = quat[3]
        marker1.pose.position.x = 0
        marker1.pose.position.y = 0
        marker1.pose.position.z = 0.5
        marker1.id = 0

        marker2 = Marker()
        marker2.header.frame_id = "catvehicle/base_link"
        marker2.type = marker2.ARROW
        marker2.action = marker2.ADD
        marker2.scale.x = 0.3
        marker2.scale.y = 0.15
        marker2.scale.z = 0.15
        marker2.color.a = 1.0
        marker2.color.r = 0.0
        marker2.color.g = 1.0
        marker2.color.b = 0.0
        marker2.pose.orientation.w = 1.0
        marker2.pose.position.x = 0.5
        marker2.pose.position.y = 0.5
        marker2.pose.position.z = 0.5
        marker2.id = 1

        
        self.markers.markers.append(marker1)
        self.markers.markers.append(marker2)

    def publish_markers(self):
        while not rospy.is_shutdown():
            self.marker_publisher.publish(self.markers)

if __name__ == '__main__':
    rospy.init_node('marker_publisher')
    pedestrian_markers = PedestrianMarkers()
    pedestrian_markers.publish_markers()




