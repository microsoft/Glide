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

        # Subscribe to haptic gesture
        self.haptic_subscriber = self.create_subscription(
            Int32,
            'microROS/haptic',
            self.haptic_callback,
            10
        )
        self.haptic_subscriber 

        self.traj_idx = 0
        self.trajectories = {
            '0': {
                'left': '',
                'right': '',
                'straight': 'traj_0_straight',
            },
            '1': {
                'left': 'traj_1_left',
                'right': '',
                'straight': 'traj_1_straight',
            },
            '2': {
                'left': 'traj_2_left',
                'right': '',
                'straight': 'traj_2_straight',
            }
        }

        print('Loading trajectories')
        traj_dir = ament_index_python.get_packages_with_prefixes()['glide_robot'].replace('install', 'src')
        for traj_idx, traj_dict in self.trajectories.items():
            for traj_direction, traj_file in traj_dict.items():
                if traj_file == '':
                    continue
                with open(traj_dir + '/trajectories/' + traj_file + '.json') as f:
                    traj_msg = json.load(f)
                    self.trajectories[traj_idx][traj_direction] = message_converter.convert_dictionary_to_ros_message('nav_msgs/Path', traj_msg)

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
        
        self.current_traj = self.trajectories['0']['straight']

        self.timer = self.create_timer(1, self.run)
        
    def haptic_callback(self, msg):
        STOP_HAPTIC_GESTURE = 1
        LEFT_HAPTIC_GESTURE = 2
        RIGHT_HAPTIC_GESTURE = 3
        print('callback')

        if msg.data == LEFT_HAPTIC_GESTURE and self.override_traj:
            print('TURN LEFT')
            self.current_traj = self.trajectories[str(self.traj_idx)]['left']
            # Do not do anything if trajectory is invalid
            if self.current_traj == '':
                return
            self.override_traj = False
            self.execute_traj = True

        elif msg.data == RIGHT_HAPTIC_GESTURE and self.override_traj:
            print('TURN RIGHT')
            self.current_traj = self.trajectories[str(self.traj_idx)]['right']
            # Do not do anything if trajectory is invalid
            if self.current_traj == '':
                return
            self.override_traj = False
            self.execute_traj = True

        elif msg.data == STOP_HAPTIC_GESTURE and self.override_traj:
            print('STOP')
            self.execute_traj = True
            self.override_traj = True
            self.current_traj = self.trajectories[str(self.traj_idx)]['straight']
            # Do not do anything if trajectory is invalid
            if self.current_traj == '':
                return

            self.override_traj = True
            
            sleep(2) # pause between updating trajectory and releasing brakes
        
        # Release brakes
        twist = Twist()
        twist.linear.x = -1.0
        twist.angular.z = 0.0
        self.cmdvel_publisher.publish(twist)

    def execute_plan(self):
        self.navigator.clearLocalCostmap()
        # self.navigator.cancelNav()

        self.path_publisher.publish(self.current_traj)
        self.path_publisher.publish(self.current_traj)

        self.navigator.goThroughPoses(self.current_traj)
        feedback = self.navigator.getFeedback()
        i = 0
        while not self.navigator.isNavComplete():
            if self.override_traj:
                self.navigator.clearLocalCostmap()
                self.navigator.cancelNav()
                return None

            feedback = self.navigator.getFeedback()
            if feedback and i % 5 == 0:
                print('Distance remaining: ' + '{:.2f}'.format(
                    feedback.distance_to_goal) + ' meters.')
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
                self.traj_idx += 1
                self.override_traj = True
                print('Goal succeeded!')
                self.current_traj = self.trajectories[str(self.traj_idx)]['straight']
                return
            elif result == NavigationResult.CANCELED:
                print('Goal was canceled!')
            elif result == NavigationResult.FAILED:
                print('Goal failed!')
                if feedback.distance_to_goal > 0.5:
                    self.navigator.clearLocalCostmap()
                    self.navigator.cancelNav()
                    print('Retrying...')
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
    # navigator.waitUntilNav2Active()
    # navigator.clearLocalCostmap()

    experimentNode = ExperimentB(navigator)
    experimentNode.run()

    rclpy.spin(experimentNode)

    twist = Twist()
    twist.linear.x = -1.0
    twist.angular.z = 0.0
    experimentNode.cmdvel_publisher.publish(twist)
    experimentNode.cmdvel_publisher.publish(twist)

    experimentNode.destroy_node()
