from nav_msgs.msg import Path
from ros2_message_converter import message_converter
from robot_navigator import BasicNavigator, NavigationResult
import ament_index_python
import argparse
import json 
import rclpy
from rclpy.node import Node
from time import sleep

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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--traj_file', help="Name of the file in the trajectories subdirectory")
    args = parser.parse_args()

    traj_dir = ament_index_python.get_packages_with_prefixes()['glide_robot'].replace('install', 'src')
    with open(traj_dir + '/trajectories/' + args.traj_file) as f:
        json_msg = json.load(f)

    ros_msg = message_converter.convert_dictionary_to_ros_message('nav_msgs/Path', json_msg)

    rclpy.init()

    node = rclpy.create_node('path_pub')
    publisher = node.create_publisher(Path, 'plan', 10)
    while rclpy.ok():
        publisher.publish(ros_msg)
        sleep(0.5)
        break

    navigator = BasicNavigator()
    navigator.waitUntilNav2Active()
    navigator.clearLocalCostmap()
    navigator.goThroughPoses(ros_msg)

    i = 0
    while not navigator.isNavComplete():
        i += 1

    result = navigator.getResult()
    if result == NavigationResult.SUCCEEDED:
        print('Goal succeeded!')
    elif result == NavigationResult.CANCELED:
        print('Goal was canceled!')
    elif result == NavigationResult.FAILED:
        print('Goal failed!')
    else:
        print('Goal has an invalid return status!')