import rclpy
 
from rclpy.node import Node
 
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

import serial
 
class TeensySerialHubPublisher(Node):
  def __init__(self):
    super().__init__('TeensySerialHubPublisher')

    self.declare_parameter('device', '/dev/ttyACM0')

    self.ser = serial.Serial(self.device_name,
                      230400,
                      timeout=.1)

    # with serial.threaded.ReaderThread(ser, TestLines) as protocol:
    #       protocol.write_line('hello')
    #       protocol.write_line('world')
    #       time.sleep(1)
    #       self.assertEqual(protocol.received_lines, ['hello', 'world'])
 
def main(args=None):
  rclpy.init(args=args)

  teensy_serial_hub_node = TeensySerialHubPublisher()

  rclpy.spin(teensy_serial_hub_node)

  teensy_serial_hub_node.destroy_node()

  rclpy.shutdown()
 
if __name__ == '__main__':
  main()
