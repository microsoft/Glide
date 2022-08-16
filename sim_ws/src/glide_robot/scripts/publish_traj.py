from nav_msgs.msg import Path
from ros2_message_converter import message_converter
from robot_navigator import BasicNavigator
import ament_index_python
import argparse
import json 
import rclpy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--traj_file', help="Name of the file in the trajectories subdirectory")
    args = parser.parse_args()

    traj_dir = ament_index_python.get_packages_with_prefixes()['glide_robot'].replace('install', 'src')
    with open(traj_dir + '/trajectories/' + args.traj_file) as f:
        json_msg = json.load(f)

    ros_msg = message_converter.convert_dictionary_to_ros_message('nav_msgs/Path', json_msg)

    rclpy.init()
    navigator = BasicNavigator()
    navigator.goThroughPoses(ros_msg)