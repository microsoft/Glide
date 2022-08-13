import rclpy
from rclpy.node import Node
from rclpy import time
from visualization_msgs.msg import MarkerArray
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import numpy as np
from nav_msgs.msg import Path 
from geometry_msgs.msg import PoseStamped
import math 
from robot_navigator import BasicNavigator, NavigationResult

class WaypointSubscriber(Node):
    def __init__(self):
        super().__init__('waypoint_subscriber')
        self.waypoints = []
        self.waypoints_sub = self.create_subscription(
            MarkerArray,
            'waypoints',
            self.listener_callback,
            10
        )
        self.xs = []
        self.ys = []

    def listener_callback(self, msg):
        marker_pose = msg.markers[-1].pose
        self.xs.append(marker_pose.position.x)
        self.ys.append(marker_pose.position.y)
        print(self.xs, self.ys)

class GlobalPlanPublisher(Node):
    def __init__(self):
        super().__init__('global_plan_publisher')
        self.publisher = self.create_publisher(
            Path,
            'plan',
            10
        )

    def publish(self, msg):
        self.publisher.publish(msg)

def get_quaternion_from_euler(roll, pitch, yaw):
  """
  Convert an Euler angle to a quaternion.
   
  Input
    :param roll: The roll (rotation around x-axis) angle in radians.
    :param pitch: The pitch (rotation around y-axis) angle in radians.
    :param yaw: The yaw (rotation around z-axis) angle in radians.
 
  Output
    :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
  """
  qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
  qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
  qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
  qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
 
  return [qx, qy, qz, qw]

if __name__ == '__main__':
    rclpy.init()
    # waypoint_sub = WaypointSubscriber()
    path_pub = GlobalPlanPublisher()
#     # rclpy.spin(waypoint_sub)
    navigator = BasicNavigator()
    # Wait for navigation to fully activate. Use this line if autostart is set to true.
    navigator.waitUntilNav2Active()

    x = [0, 0.5383138060569763, 1.33791184425354, 2.1851909160614014, 2.9529881477355957, 3.5729126930236816, 3.8657066822052, 4.004999160766602]
    y = [0, -0.04674685001373291, -0.1971738338470459, -0.3477250933647156, -0.5033672451972961, -0.478493869304657, 0.06113353371620178, 0.6541405320167542]

    plt.scatter(x, y, color='blue', label='given')

    # For this special case, the following code produces the
    # desired results. However, I need something that depends
    # only on x and y:
    from scipy import interpolate
    tck,u=interpolate.splprep([x,y],s=0.0)
    x_i,y_i= interpolate.splev(np.linspace(0,1,100),tck)
    plt.plot(x_i, y_i, color='green', label='desired')

    clock = time.Time()
    path = []
    for i in range(len(x_i)-1): 
        theta = np.arctan((y_i[i+1] - y_i[i])/(x_i[i+1] - x_i[i]))
        q = get_quaternion_from_euler(0, 0, theta)

        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = time.Time(seconds=31).to_msg()
        pose.pose.position.x = x_i[i]
        pose.pose.position.y = y_i[i]
        pose.pose.position.z = 0.0
        pose.pose.orientation.x = q[0]
        pose.pose.orientation.y = q[1]
        pose.pose.orientation.z = q[2]
        pose.pose.orientation.w = q[3]
        path.append(pose)

    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = time.Time(seconds=31).to_msg()
    pose.pose.position.x = x_i[-1]
    pose.pose.position.y = y_i[-1]
    pose.pose.position.z = 0.0
    pose.pose.orientation.x = q[0]
    pose.pose.orientation.y = q[1]
    pose.pose.orientation.z = q[2]
    pose.pose.orientation.w = q[3]
    path.append(pose)

    global_plan = Path()
    global_plan.header.frame_id = 'map'
    global_plan.header.stamp = time.Time().to_msg()
    global_plan.poses = path

    path_pub.publish(global_plan)
    navigator.goThroughPoses(global_plan)
    print('published')
    # import IPython; IPython.embed()

    # plt.legend()
    # plt.show()

