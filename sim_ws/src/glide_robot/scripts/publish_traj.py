from nav_msgs.msg import Path
from ros2_message_converter import message_converter
from robot_navigator import BasicNavigator, NavigationResult
import ament_index_python
import argparse
import json 
import rclpy
from rclpy.node import Node
from time import sleep
from geometry_msgs.msg import PoseStamped

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

def execute_plan(navigator, plan):
    navigator.goThroughPoses(plan)
    feedback = navigator.getFeedback()
    i = 0
    while not navigator.isNavComplete():
        feedback = navigator.getFeedback()
        if feedback and i % 5 == 0:
            print('Distance remaining: ' + '{:.2f}'.format(
                feedback.distance_to_goal) + ' meters.')
        i += 1
    return feedback

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
    # rclpy.spin_once(publisher, timeout_sec=1.0)

    navigator = BasicNavigator()
    navigator.waitUntilNav2Active()
    navigator.clearAllCostmaps()

    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    initial_pose.pose.position.x = 0.0
    initial_pose.pose.position.y = 0.0
    initial_pose.pose.position.z = 0.0
    initial_pose.pose.orientation.x = 0.0
    initial_pose.pose.orientation.y = 0.0
    initial_pose.pose.orientation.z = -0.7071068
    initial_pose.pose.orientation.w = 0.7071068
    navigator.setInitialPose(initial_pose)

    max_retries = 1000
    num_retries = 0
    retry = True

    try:
        while retry == True and num_retries < max_retries:
            feedback = execute_plan(navigator, ros_msg)
            result = navigator.getResult()
            if result == NavigationResult.SUCCEEDED:
                print('Goal succeeded!')
                break
            elif result == NavigationResult.CANCELED:
                print('Goal was canceled!')
                retry = False
            elif result == NavigationResult.FAILED:
                print('Goal failed!')
                if feedback and feedback.distance_to_goal > 0.5:
                    # retry = True
                    # navigator.clearLocalCostmap()
                    # navigator.cancelNav()
                    # num_retries += 1
                    print('Retrying...')
            else:
                print('Goal has an invalid return status!')
    except KeyboardInterrupt:
        navigator.cancelNav()
        # navigator.lifecycleShutdown()
        navigator.destroy_node()
        # rclpy.shutdown()
        exit(0)
        
    # navigator.lifecycleShutdown()
    navigator.destroy_node()
    # rclpy.shutdown()
    exit(0)