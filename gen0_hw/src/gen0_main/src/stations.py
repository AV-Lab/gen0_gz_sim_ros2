#!/usr/bin/python3


import rospy
from geometry_msgs.msg import PoseStamped

def publish_goal():
    rospy.init_node('goal_publisher', anonymous=False)
    pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)

    # Create a PoseStamped message
    goal = PoseStamped()
    goal.header.frame_id = "map"  # Assuming the goal is specified in the "map" frame
    goal.pose.position.x = 47.85  # X-coordinate of the goal
    goal.pose.position.y = -27.89  # Y-coordinate of the goal
    goal.pose.orientation.z = 0  # Orientation of the goal
    goal.pose.orientation.w = 1.0  # Orientation of the goal

    # Publish the goal
    pub.publish(goal)
    rospy.loginfo("Published the goal")

if __name__ == '__main__':
    try:
        publish_goal()
    except rospy.ROSInterruptException:
        pass

