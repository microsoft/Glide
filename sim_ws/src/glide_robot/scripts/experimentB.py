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

class ExperimentB(Node):
    def __init__(self, navigator):
        super().__init__('experiment_B')

        self.navigator = navigator
        self.override_traj = True
        self.execute_traj = True
        self.engage_slowdown_haptic = True
        self.init_dist_to_goal = 0

        # Publishing global plan
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

        # Publishing haptic gestures
        self.haptic_publisher = self.create_publisher(
            Int32,
            'microROS/haptic',
            10
        )

        # Subscribe to haptic gesture
        self.haptic_subscriber = self.create_subscription(
            Int32,
            'microROS/haptic',
            self.haptic_callback,
            10
        )
        self.haptic_subscriber 

        self.trajectories_dict = {
            'start': {
                'left': '',
                'right': '',
                'straight': 'traj_0_straight'
            },
            'traj_0_straight': {
                'left': 'traj_1_left',
                'right': '',
                'straight': '',
            },
            'traj_1_left': {
                'left': 'traj_2_left',
                'right': '',
                'straight': 'traj_2_straight',
            },
            'traj_2_left': {
                'left': 'traj_3_left',
                'right': 'traj_3_right',
                'straight': ''
            },
            'traj_2_straight': {
                'left': 'traj_4_left',
                'right': '',
                'straight': ''
            }, 'traj_4_left': {
                'left': '',
                'right': 'traj_5_right',
                'straight': 'traj_5_straight'
            }
        }

        print('Loading trajectories')
        self.trajectory_msgs = {}
        traj_dir = ament_index_python.get_packages_with_prefixes()['glide_robot'].replace('install', 'src')
        for traj_idx, traj_dict in self.trajectories_dict.items():
            for traj_direction, traj_file in traj_dict.items():
                if traj_file == '':
                    continue
                with open(traj_dir + '/trajectories/' + traj_file + '.json') as f:
                    traj_msg = json.load(f)
                    self.trajectory_msgs[traj_file] = message_converter.convert_dictionary_to_ros_message('nav_msgs/Path', traj_msg)

        initial_pose = PoseStamped()
        initial_pose.header.frame_id = 'map'
        initial_pose.header.stamp = self.navigator.get_clock().now().to_msg()
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
        
        self.traj_idx = 'start'
        self.current_traj = self.trajectory_msgs['traj_0_straight']

        self.timer = self.create_timer(1, self.run)
        
    def haptic_callback(self, msg):
        STOP_HAPTIC_GESTURE = 1
        LEFT_HAPTIC_GESTURE = 2
        RIGHT_HAPTIC_GESTURE = 3
        print('callback')

        if msg.data == LEFT_HAPTIC_GESTURE and self.override_traj:
            print('TURN LEFT')
            traj_idx = self.trajectories_dict[self.traj_idx]['left']
            # Do not do anything if trajectory is invalid
            if not self.valid_direction(traj_idx):
                return
            self.traj_idx = traj_idx
            self.current_traj = self.trajectory_msgs[self.traj_idx]
            self.override_traj = False
            self.execute_traj = True

        elif msg.data == RIGHT_HAPTIC_GESTURE and self.override_traj:
            print(self.traj_idx)
            traj_idx = self.trajectories_dict[self.traj_idx]['right']
            # Do not do anything if trajectory is invalid
            if not self.valid_direction(traj_idx):
                return
            self.traj_idx = traj_idx
            self.current_traj = self.trajectory_msgs[self.traj_idx]
            self.override_traj = False
            self.execute_traj = True

        elif msg.data == STOP_HAPTIC_GESTURE:
            print('STOP')
            return
        
        # Release brakes
        twist = Twist()
        twist.linear.x = -1.0
        twist.angular.z = 0.0
        self.cmdvel_publisher.publish(twist)

    def valid_direction(self, traj_idx):
        # If inputted direction valid return
        if traj_idx != '':
            return True

        # If the inputted direction is invalid engage brakes
        if traj_idx == '':
            twist = Twist()
            twist.linear.x = 1.0
            twist.angular.z = 0.0
            self.cmdvel_publisher.publish(twist)
        
            # Default to going straight if valid
            traj_idx = self.trajectories_dict[self.traj_idx]['straight']
            if traj_idx != '':
                sleep(2)
                twist.linear.x = -1.0
                self.cmdvel_publisher.publish(twist)

        return False

    def check_progress(self, distance):
        diff = self.init_dist_to_goal - distance

        # Hack for when initial distance_to_goal is incorrect
        if diff < 0:
            self.init_dist_to_goal = distance

        if self.init_dist_to_goal - distance > 0.25:
            self.traj_idx = self.trajectories_dict[self.traj_idx]['straight']
            self.override_traj = False
            self.init_dist_to_goal = 0

    def execute_plan(self):
        if self.current_traj == '':
            return None
            
        # self.navigator.clearLocalCostmap()
        # self.navigator.cancelNav()
        
        self.path_publisher.publish(self.current_traj)
        self.path_publisher.publish(self.current_traj)

        self.navigator.goThroughPoses(self.current_traj)
        feedback = self.navigator.getFeedback()
        i = 0
        while not self.navigator.isNavComplete():
            feedback = self.navigator.getFeedback()
            if feedback and feedback.distance_to_goal < 1.5 and self.engage_slowdown_haptic:
                print('SLOW DOWN')
                self.engage_slowdown_haptic = False
                gesture = Int32()
                gesture.data = 1
                self.haptic_publisher.publish(gesture)
                self.haptic_publisher.publish(gesture)

            if feedback and i % 5 == 0:
                print('Distance remaining: ' + '{:.2f}'.format(
                    feedback.distance_to_goal) + ' meters.')

            if self.override_traj:
                print(self.init_dist_to_goal, i)
                if feedback and self.init_dist_to_goal == 0 and i == 0:
                    self.init_dist_to_goal = feedback.distance_to_goal

                if feedback:
                    self.check_progress(feedback.distance_to_goal)

                # self.navigator.clearLocalCostmap()
                self.navigator.cancelNav()
                return None

            i += 1

        return feedback

    def run(self):
        try:
            if not self.execute_traj:
                return
            feedback = self.execute_plan()
            # Re-execute plan with new trajectory
            if feedback == None:
                return

            result = self.navigator.getResult()
            if result == NavigationResult.SUCCEEDED:
                # Engage brakes
                twist = Twist()
                twist.linear.x = 1.0
                twist.angular.z = 0.0
                self.cmdvel_publisher.publish(twist)
                self.execute_traj = False
                self.override_traj = True
                print('Goal succeeded!')
                self.current_traj = ''

                print(self.traj_idx)
                traj_idx = self.trajectories_dict[self.traj_idx]['straight']
                if traj_idx != '':
                    self.execute_traj = True
                    sleep(2)
                    # Release brakes
                    twist = Twist()
                    twist.linear.x = -1.0
                    twist.angular.z = 0.0
                    self.cmdvel_publisher.publish(twist)
                    self.current_traj = self.trajectory_msgs[traj_idx]
                
                self.engage_slowdown_haptic = True

                # if self.traj_idx == "traj_2_left":
                #     initial_pose = PoseStamped()
                #     initial_pose.header.frame_id = 'map'
                #     initial_pose.header.stamp = self.navigator.get_clock().now().to_msg()
                #     initial_pose.pose.position.x = 7.38787
                #     initial_pose.pose.position.y = 16.8
                #     initial_pose.pose.position.z = 0.0
                #     initial_pose.pose.orientation.x = 0.0
                #     initial_pose.pose.orientation.y = 0.0
                #     initial_pose.pose.orientation.z = 0.7071068
                #     initial_pose.pose.orientation.w = 0.7071068
                #     self.navigator.setInitialPose(initial_pose)
                #     self.navigator.setInitialPose(initial_pose)

                return
            elif result == NavigationResult.CANCELED:
                print('Goal was canceled!')
            elif result == NavigationResult.FAILED:
                print('Goal failed!')
                # if feedback.distance_to_goal > 0.5:
                #     self.navigator.clearLocalCostmap()
                #     self.navigator.cancelNav()
                #     print('Retrying...')
            else:
                print('Goal has an invalid return status!')
        except KeyboardInterrupt:
            twist = Twist()
            twist.linear.x = -1.0
            twist.angular.z = 0.0
            self.cmdvel_publisher.publish(twist)
            self.cmdvel_publisher.publish(twist)
            sleep(2)
            self.navigator.cancelNav()
            self.navigator.destroy_node()
            exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--traj_file', help="Name of the file in the trajectories subdirectory")
    args = parser.parse_args()

    rclpy.init()

    # node = rclpy.create_node('path_pub')
    # publisher = node.create_publisher(Path, 'plan', 10)
    # while rclpy.ok():
    #     publisher.publish(ros_msg)
    #     sleep(0.5)
        # break
    # rclpy.spin_once(publisher, timeout_sec=1.0)

    navigator = BasicNavigator()
    navigator.waitUntilNav2Active()
    navigator.clearAllCostmaps()

    experimentNode = ExperimentB(navigator)
    experimentNode.run()

    rclpy.spin(experimentNode)

    twist = Twist()
    twist.linear.x = -1.0
    twist.angular.z = 0.0
    experimentNode.cmdvel_publisher.publish(twist)
    experimentNode.cmdvel_publisher.publish(twist)

    experimentNode.destroy_node()
