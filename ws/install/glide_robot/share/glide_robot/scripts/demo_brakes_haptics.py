from rclpy.node import Node
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
import rclpy

class DemoBrakesHaptics(Node):
    def __init__(self):
        super().__init__('demo_brakes_haptics')

        # Publishing haptic gestures
        self.haptic_publisher = self.create_publisher(
            Int32,
            'microROS/haptic',
            10
        )

        # Publishing velocities
        self.cmdvel_publisher = self.create_publisher(
            Twist,
            'cmd_vel',
            10
        )

    def demo(self):
        while True:
            value = input()
            if value == 's':
                gesture = Int32()
                gesture.data = 1
                self.haptic_publisher.publish(gesture)
            elif value == 'l':
                gesture = Int32()
                gesture.data = 2
                self.haptic_publisher.publish(gesture)
            elif value == 'r':
                gesture = Int32()
                gesture.data = 3
                self.haptic_publisher.publish(gesture)
            elif value == 'b':
                twist = Twist()
                twist.linear.x = 1.0
                twist.angular.z = 0.0
                self.cmdvel_publisher.publish(twist)
            elif value == 'u':
                twist = Twist()
                twist.linear.x = -1.0
                twist.angular.z = 0.0
                self.cmdvel_publisher.publish(twist)
            elif value == 'e':
                exit(0)
            else:
                print('Invalid input')

if __name__ == '__main__':
    rclpy.init()

    demoNode = DemoBrakesHaptics()
    demoNode.demo()

    rclpy.spin(demoNode)

    demoNode.destroy_node()
    rclpy.shutdown()
    exit(0)
