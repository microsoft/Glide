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
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist

class ExperimentA(Node):
    def __init__(self, navigator, path):
        super().__init__('experiment_A')
        
        self.navigator = navigator
        self.path = path 

        # Publishing haptic gestures
        self.haptic_publisher = self.create_publisher(
            Int32,
            'microROS/haptic',
            10
        )

        self.path_publisher = self.create_publisher(
            Path, 
            'plan', 
            10
        )

        # Publishing velocities
        self.cmdvel_publisher = self.create_publisher(
            Twist,
            'cmd_vel',
            10
        )

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
        self.navigator.setInitialPose(initial_pose)
        
        twist = Twist()
        twist.linear.x = -1.0
        twist.angular.z = 0.0
        self.cmdvel_publisher.publish(twist)
        
        self.run()

    def execute_plan(self):
        self.navigator.goThroughPoses(self.path)
        feedback = self.navigator.getFeedback()
        i = 0
        while not self.navigator.isNavComplete():
            feedback = self.navigator.getFeedback()
            if feedback and i % 5 == 0:
                print('Distance remaining: ' + '{:.2f}'.format(
                    feedback.distance_to_goal) + ' meters.')
            i += 1
        return feedback

    def run(self):
        publish_slowdown_gesture = True
        while True:
            feedback = self.execute_plan()
            if feedback and publish_slowdown_gesture and feedback.distance_to_goal < 2.0:
                gesture = Int32()
                gesture.data = 1
                self.haptic_publisher.publish(gesture)
                publish_slowdown_gesture = False

            result = navigator.getResult()
            if result == NavigationResult.SUCCEEDED:
                print('Goal succeeded!')

                # Engage brakes
                twist = Twist()
                twist.linear.x = 1.0
                twist.angular.z = 0.0
                self.cmdvel_publisher.publish(twist)
            
                sleep(2)
                
                # Release brakes
                twist = Twist()
                twist.linear.x = -1.0
                twist.angular.z = 0.0
                self.cmdvel_publisher.publish(twist)

                self.navigator.cancelNav()
                self.navigator.destroy_node()
                exit(0)
            elif result == NavigationResult.CANCELED:
                print('Goal was canceled!')
            elif result == NavigationResult.FAILED:
                print('Goal failed!')
                print('Retrying...')
            else:
                print('Goal has an invalid return status!')
            
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
    navigator.waitUntilNav2Active()
    navigator.clearAllCostmaps()

    experimentNode = ExperimentA(navigator, ros_msg)

    rclpy.spin(experimentNode)

    navigator.cancelNav()
    navigator.destroy_node()
    exit(0)