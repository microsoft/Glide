import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Int32 
import message_filters
from sensor_msgs.msg import Imu
import math
from rclpy.clock import Clock
import numpy as np
from geometry_msgs.msg import TransformStamped
from tf2_ros.transform_broadcaster import TransformBroadcaster

def get_quaternion_from_euler(roll, pitch, yaw):
    """
    Convert an Euler angle to a quaternion.
    
    Input
        :param roll: The roll (rotation around x-axis) angle in radians.
        :param pitch: The pitch (rotation around y-axis) angle in radians.
        :param yaw: The yaw (rotation around z-axis) angle in radians.
    
    Output
        :return qx, qy, qz, qw: The orientation in quaternion [x,y,z,w] format
    """
    qx = np.sin(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) - np.cos(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    qy = np.cos(roll/2) * np.sin(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.cos(pitch/2) * np.sin(yaw/2)
    qz = np.cos(roll/2) * np.cos(pitch/2) * np.sin(yaw/2) - np.sin(roll/2) * np.sin(pitch/2) * np.cos(yaw/2)
    qw = np.cos(roll/2) * np.cos(pitch/2) * np.cos(yaw/2) + np.sin(roll/2) * np.sin(pitch/2) * np.sin(yaw/2)
    
    return [qx, qy, qz, qw]

def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians

class WheelOdomNode(Node):
    def __init__(self):
        super().__init__("WheelOdomNode")
        # self.odom_broadcaster = TransformBroadcaster(self)
        self.odom_publisher = self.create_publisher(Odometry, '/wheel/odometry', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)

        self.left_wheel_enc_sub = message_filters.Subscriber(self, Int32, '/microROS/odometry_left')
        self.left_m_per_pulse = 0.0008165846
        
        self.right_wheel_enc_sub = message_filters.Subscriber(self, Int32, '/microROS/odometry_right')
        self.right_m_per_pulse = 0.00082122518

        self.imu_sub = message_filters.Subscriber(self, Imu, '/imu/data')

        self.wheel_enc_sub = message_filters.ApproximateTimeSynchronizer([self.left_wheel_enc_sub, self.right_wheel_enc_sub, self.imu_sub], 5, 0.2, allow_headerless=True)
        self.wheel_enc_sub.registerCallback(self.compute_odom)

        self.odom = Odometry()
        self.odom_tf = TransformStamped()
        self.odom_tf.header.frame_id = "odom"
        self.odom_tf.child_frame_id = "base_footprint"
        self.x = 0
        self.y = 0
        self.th = 0

        self.current_time = Clock().now().to_msg()
        self.last_time = Clock().now().to_msg()

    def timer_callback(self):
        self.odom_publisher.publish(self.odom)
        # self.odom_broadcaster.sendTransform(self.odom_tf)

    def compute_odom(self, left_enc, right_enc, imu):
        self.current_time = Clock().now().to_msg()
        dt = self.current_time.sec - self.last_time.sec
        v_l = left_enc.data * self.left_m_per_pulse
        v_r = right_enc.data * self.right_m_per_pulse
        _, _, th = euler_from_quaternion(imu.orientation.x, imu.orientation.y, imu.orientation.z, imu.orientation.w)

        vx = (v_l + v_r)/2
        vth = (v_l - v_r)/0.2332482

        self.x += vx * math.cos(self.th) * dt
        self.y += vx * math.sin(self.th) * dt
        self.th += vth * dt

        qx, qy, qz, qw = get_quaternion_from_euler(0, 0, self.th)

        # odom_tf = TransformStamped()
        # odom_tf.header.stamp = self.current_time
        # odom_tf.header.frame_id = "odom"
        # odom_tf.child_frame_id = "base_footprint"
        # odom_tf.transform.translation.x = self.x
        # odom_tf.transform.translation.y = self.y
        # odom_tf.transform.translation.z = 0.0
        # odom_tf.transform.rotation.x = qx
        # odom_tf.transform.rotation.y = qy
        # odom_tf.transform.rotation.z = qz
        # odom_tf.transform.rotation.w = qw
        # self.odom_tf = odom_tf

        time_stamp = Clock().now().to_msg()
        odom = Odometry()
        odom.header.stamp = self.current_time
        odom.header.frame_id = "odom"

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        odom.pose.pose.orientation.x = qx
        odom.pose.pose.orientation.y = qy
        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw

        odom.child_frame_id = "base_footprint"
        odom.twist.twist.linear.x = vx
        odom.twist.twist.angular.z = vth
        self.odom = odom
        
        self.last_time = self.current_time

def main(args=None):
    rclpy.init(args=args)

    wheel_odom_node = WheelOdomNode()
    
    rclpy.spin(wheel_odom_node)
    
    wheel_odom_node.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()    

