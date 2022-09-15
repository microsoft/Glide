import rclpy

from rclpy.node import Node
 
from std_msgs.msg import Float32, Int32
from geometry_msgs.msg import Twist

class TorqueToHapticsPublisher(Node):
  def __init__(self):
    super().__init__('TorqueToHapticsPublisher')
     
    self.publisher_haptic = self.create_publisher(
        Int32,
        '/microROS/haptic',
        10)

    self.subscription = self.create_subscription(
        Int32,
        'microROS/torque',
        self.torque_callback,
        10)
        
    self.subscription  # prevent unused variable warning
    self.last_torque = 250

  def torque_callback(self, msg):
    LEFT_TORQUE_THRESHOLD = 150
    RIGHT_TORQUE_THRESHOLD = 350
    LEFT_HAPTIC_GESTURE = 2
    RIGHT_HAPTIC_GESTURE = 3

    torque = msg.data

    msg_channel_haptic = Int32()

    # Check last torque value so gesture does not continually publish
    if torque <= LEFT_TORQUE_THRESHOLD and self.last_torque > LEFT_TORQUE_THRESHOLD:
        msg_channel_haptic.data = LEFT_HAPTIC_GESTURE
        self.publisher_haptic.publish(msg_channel_haptic)
        #self.publisher_haptic.publish(msg_channel_haptic)
    elif torque >= RIGHT_TORQUE_THRESHOLD and self.last_torque < RIGHT_TORQUE_THRESHOLD:
        msg_channel_haptic.data = RIGHT_HAPTIC_GESTURE
        self.publisher_haptic.publish(msg_channel_haptic)
        #self.publisher_haptic.publish(msg_channel_haptic)

    #self.get_logger().info(f'Torque: "{torque}"')
    self.last_torque = torque

def main(args=None):
  rclpy.init(args=args)

  torque_to_haptics_node = TorqueToHapticsPublisher()

  rclpy.spin(torque_to_haptics_node)

  torque_to_haptics_node.destroy_node()

  rclpy.shutdown()
 
if __name__ == '__main__':
  main()
