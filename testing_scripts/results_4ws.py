import rospy
from std_msgs.msg import Header
import time
from nav_msgs.msg import Odometry
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


def data_callback(data):
    xs.append(float(data.pose.pose.position.x))
    ys.append(float(data.pose.pose.position.y))
    # Plot the data
    plt.scatter(xs, ys)
    plt.xlabel('X-axis label')
    plt.ylabel('Y-axis label')
    plt.title('Live Plot')
    plt.xlim([-50, 50])
    plt.ylim([-50, 50])
    plt.draw()
    plt.pause(0.001) 


rospy.Subscriber("odom", Odometry, data_callback)
# style.use('fivethirtyeight')
# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)
xs = []
ys = []
plt.show()

if __name__ == '__main__':
    rospy.init_node('results_4ws', anonymous=True)
    rospy.spin()
