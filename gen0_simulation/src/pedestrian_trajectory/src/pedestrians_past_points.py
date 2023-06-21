#!/usr/bin/env python3

import rospy
from gazebo_msgs.msg import ModelStates
from geometry_msgs.msg import Point, PoseArray, Pose
import sys
from visualization_msgs.msg import Marker, MarkerArray
import tf
import math
from copy import deepcopy


class PedestrianPastPoints:
    def __init__(self, names, frequency, points):
        self.data = None
        self.sub = rospy.Subscriber('gazebo/model_states', ModelStates, self.callback)
        self.marker_publisher = rospy.Publisher('visualization_marker', Marker, queue_size=10)
        self.pedestrian_publisher = rospy.Publisher('pedestrian_past_position', PoseArray, queue_size=10)
        self.rate = rospy.Rate(int(frequency))
        self.points= points
        self.names= names
        self.counter=0
        self.marker = Marker()
        self.markers = [MarkerArray() for size in range(len(names))]
        self.pose_array = PoseArray()
        self.frame=0
        self.pose= Pose()
        self.points = [[[0 for col in range(3)] for row in range(2)] for depth in range(len(names))] # three dimensional list to store current position and previous position
        while not rospy.is_shutdown():
            self.getPosition()
            for i in range(len(self.markers)):
                if ((len(self.markers[i].markers)-1) >= 0):
                    self.marker_publisher.publish(self.markers[i].markers[len(self.markers[i].markers)-1])
                if len(self.markers[i].markers) == int(points):
                    self.markers[i].markers= []
            self.pose_array.header.frame_id= str(self.frame)
            print(self.pose_array)
            self.pedestrian_publisher.publish(self.pose_array)
            self.pose_array.poses=[]
            self.frame = self.frame + 1
            self.rate.sleep()

    def callback(self,data):
        self.data = data

    def getPosition(self):
        if self.data:
            try:
                idx_car = self.data.name.index("catvehicle")
                position_car = self.data.pose[idx_car].position
                orientation_car = self.data.pose[idx_car].orientation
                for p in range(0, len(self.names)):
                    idx_actor = self.data.name.index(self.names[p]) # Get the ID of pedestrian in gazebo
                    position_actor = self.data.pose[idx_actor].position
                    roll,pitch,yaw= tf.transformations.euler_from_quaternion([orientation_car.x, orientation_car.y, orientation_car.z, orientation_car.w])
                    self.publishMarker(p, position_actor.x - position_car.x, position_actor.y - position_car.y, position_actor.z - position_car.z, yaw)
            except ValueError:
                print("Model not found")
        else:
            print("Data not received yet.")

    def publishMarker(self, index, x, y, z, yaw):
        x1=x
        x=(x*math.cos(yaw)) + (y*math.sin(yaw))
        y= y*math.cos(yaw) + (-x1*math.sin(yaw)) 
        self.points[index][1]= self.points[index][0] # previous points will become current
        self.points[index][0]= [x, y, z] # new points
        angle = math.atan2(y- self.points[index][1][1], x - self.points[index][1][0])

        self.marker.header.frame_id = "catvehicle/base_link"
        self.marker.type = self.marker.SPHERE
        self.marker.action = self.marker.ADD
        self.marker.scale.x = 0.1
        self.marker.scale.y = 0.1
        self.marker.scale.z = 0.1
        self.marker.color.a = 1.0
        self.marker.color.r = 1.0
        self.marker.color.g = 0.0
        self.marker.color.b = 0.0
        # quat = tf.transformations.quaternion_from_euler(0, 0, angle)
        # marker.pose.orientation.x = quat[0]
        # marker.pose.orientation.y = quat[1]
        # marker.pose.orientation.z = quat[2]
        # marker.pose.orientation.w = quat[3]

        self.marker.pose.position.x = x
        self.marker.pose.position.y = y
        self.marker.pose.position.z = z
        self.marker.id = len(self.markers[index].markers) + (index * int(points))
        self.markers[index].markers.append(deepcopy(self.marker))
        self.pose=self.marker.pose
        self.pose.position.z=float(index)
        self.pose_array.poses.append(deepcopy(self.pose))


if __name__ == '__main__':
    rospy.init_node('pedestrians_past_points')
    pedestrians_names = sys.argv[1].split(",")
    frequency = sys.argv[2]
    points = sys.argv[3]
    print(pedestrians_names)
    PedestrianPastPoints(pedestrians_names, frequency, points)
