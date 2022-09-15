import rclpy

from rclpy.node import Node
 
from std_msgs.msg import Float32, Int32
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy

class CmdvelToServoPublisher(Node):
  def __init__(self):
    super().__init__('CmdvelToServoPublisher')
     
    # Steering servo
    self.publisher_channel_0 = self.create_publisher(
      Float32, 
      '/servo/channel_0',
      10)

    # Left servo
    self.publisher_channel_1 = self.create_publisher(
      Float32, 
      '/servo/channel_1',
      10)

    # Right servo
    self.publisher_channel_2 = self.create_publisher(
      Float32, 
      '/servo/channel_2',
      10)
    
    self.publisher_haptic = self.create_publisher(
        Int32,
        '/microROS/haptic',
        10)

    self.subscription = self.create_subscription(
        Twist,
        'cmd_vel',
        self.cmdvel_callback,
        10)
        
    self.subscription  # prevent unused variable warning

  def cmdvel_callback(self, msg):
    BRAKING_HAPTIC_THRESHOLD = 1
    BRAKING_HAPTIC_GESTURE = 1 # Maps to breaking gesture in microros.ino

    throttle=msg.linear.x
    steering=msg.angular.z
    if steering < -1.0:
        steering = -1.0
    elif steering > 1.0:
        steering = 1.0

    #self.get_logger().info(f'Throttle: "{throttle}"')
    self.get_logger().info(f'Steering: "{steering}"')

    msg_channel_0 = Float32()
    msg_channel_1 = Float32()
    msg_channel_2 = Float32()
 
    msg_channel_0.data = steering

    if throttle >= BRAKING_HAPTIC_THRESHOLD:
        msg_channel_haptic = Int32()
        msg_channel_haptic.data = BRAKING_HAPTIC_GESTURE
        self.publisher_haptic.publish(msg_channel_haptic)

    # -1 release servo; 1 brake servo
    if steering == 0.0 and abs(throttle) == 1.0:
        msg_channel_1.data = -1*throttle
        msg_channel_2.data = throttle
        self.publisher_channel_1.publish(msg_channel_1)
        self.publisher_channel_2.publish(msg_channel_2)
        self.publisher_channel_1.publish(msg_channel_1)
        self.publisher_channel_2.publish(msg_channel_2)
        self.get_logger().info(f'Throttle: "{throttle}"')

    # self.get_logger().info(f'Servo Channels: 0 -> "{msg_channel_0.data}" 1 -> "{msg_channel_1.data}" 2 -> "{msg_channel_2.data}"')
     
    self.publisher_channel_0.publish(msg_channel_0)
    self.publisher_channel_0.publish(msg_channel_0)
 
def main(args=None):
  rclpy.init(args=args)

  cmdvel_to_servo_node = CmdvelToServoPublisher()

  rclpy.spin(cmdvel_to_servo_node)

  cmdvel_to_servo_node.destroy_node()

  rclpy.shutdown()
 
if __name__ == '__main__':
  main()
