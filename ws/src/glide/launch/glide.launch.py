import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, GroupAction,
                            IncludeLaunchDescription, SetEnvironmentVariable)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node

def generate_launch_description():
    # ros2 launch ros_qwiic_servo qwiic.launch.py
    ros_qwiic_servo = Node(
            package='ros_qwiic_servo',
            executable='ros_qwiic_servo',
            name='ros_qwiic_servo',
            output='screen',
            parameters=[
               {'bus': '/dev/i2c-8'},
            ]
        )

    # ros2 launch realsense2_camera rs_launch.py
    realsense2_camera_dir = get_package_share_directory('realsense2_camera')
    realsense2_camera = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([realsense2_camera_dir, '/launch/rs_launch.py'])
        )

    # ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyACM0
    micro_ros_agent = Node(
            package='micro_ros_agent',
            executable='micro_ros_agent',
            name='micro_ros_agent',
            output='screen',
            arguments=["serial", "--dev", "/dev/ttyACM0"]
        )

    # ros2 run cmdvel_to_servo cmdvel_to_servo_node
    cmdvel_to_servo = Node(
            package='cmdvel_to_servo',
            executable='cmdvel_to_servo_node',
            name='cmdvel_to_servo',
            output='screen',
            parameters=[
                {'bus': '/dev/i2c-8'},
            ]
        )

    ros_qwiic_icm_20948 = Node(
            package='ros_qwiic_ICM_20948',
            executable='ros_qwiic_icm_20948',
            name='ros_qwiic_icm_20948',
            output='screen',
            parameters=[
                {'bus': '/dev/i2c-8'},
            ]
        )

    # ros2 launch imu_filter_madgwick imu_filter.launch.py
    imu_filter_madgwick_dir = get_package_share_directory('imu_filter_madgwick')
    imu_filter_madgwick = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([imu_filter_madgwick_dir, '/launch/imu_filter.launch.py'])
        )

    ros_qwiic_tof = Node(
            package='ros_qwiic_tof',
            executable='ros_qwiic_tof',
            name='ros_qwiic_tof',
            output='screen',
            parameters=[
                {'bus': '/dev/i2c-8'},
            ]
        )

    ros_qwiic_dual_encoder = Node(
            package='ros_qwiic_dual_encoder',
            executable='ros_qwiic_dual_encoder',
            name='ros_qwiic_dual_encoder',
            output='screen',
            parameters=[
                {'bus': '/dev/i2c-8'},
            ]
        )
                        
    return LaunchDescription([
        ros_qwiic_servo,
        micro_ros_agent,
        cmdvel_to_servo,
        realsense2_camera,
        # ros_qwiic_icm_20948,
        # imu_filter_madgwick,
        # ros_qwiic_dual_encoder,
        # ros_qwiic_tof
    ])