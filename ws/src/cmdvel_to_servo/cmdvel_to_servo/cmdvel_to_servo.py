import rclpy
 
from rclpy.node import Node
 
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
 
class CmdvelToServoPublisher(Node):
  def __init__(self):
    super().__init__('CmdvelToServoPublisher')
     
    self.publisher_channel_0 = self.create_publisher(
      Float32, 
      '/servo/channel_0',
      10)
    self.publisher_channel_1 = self.create_publisher(
      Float32, 
      '/servo/channel_1',
      10)
    self.publisher_channel_2 = self.create_publisher(
      Float32, 
      '/servo/channel_2',
      10)
    
    self.subscription = self.create_subscription(
        Twist,
        'cmd_vel',
        self.cmdvel_callback,
        10)
    self.subscription  # prevent unused variable warning

  def cmdvel_callback(self, msg):
    throttle=msg.linear.x
    steering=msg.angular.z

    self.get_logger().info(f'Throttle: "{throttle}"')
    self.get_logger().info(f'Steering: "{steering}"')

    msg_channel_0 = Float32()
    msg_channel_1 = Float32()
    msg_channel_2 = Float32()
 
    msg_channel_0.data = steering
    msg_channel_1.data = throttle
    msg_channel_2.data = throttle

    self.get_logger().info(f'Servo Channels: 0 -> "{msg_channel_0.data}" 1 -> "{msg_channel_1.data}" 2 -> "{msg_channel_2.data}"')
     
    self.publisher_channel_0.publish(msg_channel_0)
    self.publisher_channel_1.publish(msg_channel_1)
    self.publisher_channel_2.publish(msg_channel_2)

 
def main(args=None):
  rclpy.init(args=args)

  cmdvel_to_servo_node = CmdvelToServoPublisher()

  rclpy.spin(cmdvel_to_servo_node)

  cmdvel_to_servo_node.destroy_node()

  rclpy.shutdown()
 
if __name__ == '__main__':
  main()