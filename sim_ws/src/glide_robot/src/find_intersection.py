#! /usr/bin/env python
from math import sin, cos, pi
import threading
import rclpy
import time

from rclpy.duration import Duration
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformListener, TransformStamped, Buffer
class StatePublisher(Node):

  def __init__(self):
      rclpy.init()
      super().__init__('state_publisher')

      self.nodeName = self.get_name()
      self.get_logger().info("{0} started".format(self.nodeName))

      tfBuffer = Buffer()
      listener = TransformListener(tfBuffer, self)

      rate = rclpy.Rate(10.0)
      try:
          while rclpy.ok():
              rclpy.spin_once(self)

              now = self.get_clock().now()

              dur = Duration()
              dur.sec = 40
              dur.nsec = 0

              try:
                trans = tfBuffer.lookup_transform('base_link', 'map', now, dur )
              except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                rate.sleep()
                continue

              self.get_logger().info("\n")
              self.get_logger().info("Translation:")
              self.get_logger().info( "x:" + str( trans.transform.translation.x ) )
              self.get_logger().info( "y:" + str( trans.transform.translation.y ) )
              self.get_logger().info( "z:" + str( trans.transform.translation.z ) )


              self.get_logger().info("Rotation (in quaternion):")
              self.get_logger().info( "w:" + str( trans.transform.rotation.w ) )
              self.get_logger().info( "x:" + str( trans.transform.rotation.x ) )
              self.get_logger().info( "y:" + str( trans.transform.rotation.y ) )
              self.get_logger().info( "z:" + str( trans.transform.rotation.z ) ) 
              time.sleep(1)
      except KeyboardInterrupt:
          pass





def main():
  node = StatePublisher()

if __name__ == '__main__':
  main()