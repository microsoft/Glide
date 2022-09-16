import rclpy
from rclpy.node import Node
from rclpy.clock import Clock
from visualization_msgs.msg import MarkerArray
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
import numpy as np
from nav_msgs.msg import Path 
from geometry_msgs.msg import PoseStamped
import math 
from scipy import interpolate
from ros2_message_converter import message_converter
from std_msgs.msg import Header
from launch_ros.substitutions import FindPackageShare
import os, json 
import ament_index_python

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
        print('Waypoint added')

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

def create_spline_traj(x, y):
    tck, u = interpolate.splprep([x,y], s=0.0)
    x_i, y_i= interpolate.splev(np.linspace(0,1,300), tck)

    time_stamp = Clock().now().to_msg()
    path = []
    for i in range(len(x_i)-1): 
        theta = np.arctan((y_i[i+1] - y_i[i])/(x_i[i+1] - x_i[i]))
        q = get_quaternion_from_euler(0, 0, theta)

        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = time_stamp        
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
    pose.header.stamp = time_stamp 
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
    pose.header.stamp = time_stamp 
    global_plan.poses = path
    global_plan_json = message_converter.convert_ros_message_to_dictionary(global_plan)

    traj_name = input('Enter trajectory name: ')
    traj_dir = ament_index_python.get_packages_with_prefixes()['glide'].replace('install', 'src')
    out_path = traj_dir + '/trajectories/' + traj_name + '.json'
    with open(out_path, "w") as out:
        json.dump(global_plan_json, out)
    print('Trajectory saved to ' + out_path)

if __name__ == '__main__':
    rclpy.init()
    waypoint_sub = WaypointSubscriber()
    path_pub = GlobalPlanPublisher()
    print('Select waypoints in rviz, click CTRL+C when done')
    try:
        rclpy.spin(waypoint_sub)
    except KeyboardInterrupt:
        print('Generating Trajectory...')
        create_spline_traj(waypoint_sub.xs, waypoint_sub.ys)
        waypoint_sub.destroy_node()
        rclpy.shutdown()

