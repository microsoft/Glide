import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, GroupAction,
                            IncludeLaunchDescription, SetEnvironmentVariable)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

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
            PythonLaunchDescriptionSource([realsense2_camera_dir, '/launch/rs_launch.py']),
            launch_arguments={'align_depth': 'true', 'depth_width':'640', 'depth_height': '360', 'depth_fps':'15.0',
                'color_width':'640', 'color_height':'360','color_fps':'15.0', 'enable_gyro':'true', 'enable_accel':'true', 'unite_imu_method':'copy'}.items()
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
    )

    # ros2 run torque_to_haptics torque_to_haptics_node
    torque_to_haptics = Node(
        package='torque_to_haptics',
        executable='torque_to_haptics_node',
        name='torque_to_haptics',
        output='screen',
    )

    # ros2 run wheel_odom wheel_odom_node
    wheel_odom = Node(
        package='wheel_odom',
        executable='wheel_odom_node',
        name='wheel_odom',
        output='screen',
    )

    # ros2 run  depthimage_to_laserscan depthimage_to_laserscan_node
    param_config = os.path.join(get_package_share_directory('depthimage_to_laserscan'), 'cfg', 'param.yaml')
    depth_to_laser_scan = Node(
        package='depthimage_to_laserscan',
        executable='depthimage_to_laserscan_node',
        name='depthimage_to_laserscan_node',
        remappings=[('depth','/camera/depth/image_rect_raw'),
                    ('depth_camera_info', '/camera/depth/camera_info')],
        parameters=[param_config]
    )

    parameters=[{
          'frame_id':'base_footprint',
          'subscribe_depth':True,
          'imu_topic':'/camera/imu/sample',
          'wait_imu_to_init': True,
          'subscribe_scan': True,
          'approx_sync':False,
          "visual_odometry":True,
          "publish_null_when_lost": False,
          "Odom/ResetCountdown": "1"}]

    remappings=[
          ('rgb/image', '/camera/color/image_raw'),
          ('imu', '/imu/data'),
          ('rgb/camera_info', '/camera/color/camera_info'),
          ('depth/image', '/camera/aligned_depth_to_color/image_raw')]

    # ros2 run rtabmap_ros rgbd_odometry
    rgbd_odometry = Node(
        package='rtabmap_ros', executable='rgbd_odometry', output='screen',
        parameters=parameters,
        remappings=remappings
    )

    # ros2 run rtabmap_ros rtabmap
    rtabmap = Node(
        package='rtabmap_ros', executable='rtabmap', output='screen',
        parameters=parameters,
        remappings=remappings,
        arguments=['-d']
    )

    config_dir = os.path.join(get_package_share_directory('imu_filter_madgwick'), 'config')
    imu_filter = Node(
        package='imu_filter_madgwick',
        node_executable='imu_filter_madgwick_node',
        node_name='imu_filter',
        output='screen',
        parameters=[{
            'use_mag':False,
            'publish_tf':False,
            'world_frame':"enu"
        }],
        remappings=[('/imu/data_raw', '/camera/imu')]
    )

    pkg_share = FindPackageShare(package='glide_robot').find('glide_robot')

    # Subscribe to the joint states of the robot, and publish the 3D pose of each link.
    default_model_path = os.path.join(pkg_share, 'models/glide_description.urdf')
    model = LaunchConfiguration('model')
    declare_model_path_cmd = DeclareLaunchArgument(
        name='model',
        default_value=default_model_path,
        description='Absolute path to robot urdf file')
    state_publisher_remappings = [('/tf', 'tf'),
                                  ('/tf_static', 'tf_static')]
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        remappings=state_publisher_remappings,
        parameters=[{'use_sim_time': 'False', 
        'robot_description': Command(['xacro ', model])}],
        arguments=[default_model_path])
    
    # Start robot localization using an Extended Kalman filter
    robot_localization_file_path = os.path.join(pkg_share, 'config/ekf.yaml') 
    robot_localization = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[robot_localization_file_path,
        {'use_sim_time': 'False'}])

    static_map_path = os.path.join(pkg_share, 'maps', '99_hallway_study_final.yaml')
    map_yaml_file = LaunchConfiguration('map')
    declare_map_yaml_cmd = DeclareLaunchArgument(
        name='map',
        default_value=static_map_path,
        description='Full path to map file to load')

    nav2_params_path = os.path.join(pkg_share, 'params', 'nav2_params.yaml')
    params_file = LaunchConfiguration('params_file')
    declare_params_file_cmd = DeclareLaunchArgument(
        name='params_file',
        default_value=nav2_params_path,
        description='Full path to the ROS2 parameters file to use for all launched nodes')

    nav2_dir = FindPackageShare(package='nav2_bringup').find('nav2_bringup') 
    nav2_launch_dir = os.path.join(nav2_dir, 'launch') 
    nav2_bt_path = FindPackageShare(package='nav2_bt_navigator').find('nav2_bt_navigator')
    behavior_tree_xml_path = os.path.join(nav2_bt_path, 'behavior_trees', 'navigate_w_replanning_and_recovery.xml')
    ros2_navigation = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(os.path.join(nav2_launch_dir, 'bringup_launch.py')),
    launch_arguments = {'namespace': '',
                        'use_namespace': 'False',
                        'slam': 'False',
                        'map': map_yaml_file,
                        'use_sim_time': 'False',
                        'params_file': params_file,
                        'default_bt_xml_filename': behavior_tree_xml_path,
                        'autostart': 'True'}.items())


    # TODO: Should merge all static transforms into glide_description.urdf
    base_to_realsense = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["-0.8", "0.0175", "0.0125", "0", "0", "0", "base_link", "camera_link"]
    )
   
    base_to_front_left_wheel = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["-0.0619", "0.1317", "0.107", "0", "0", "1.57", "base_link", "front_left_wheel"]
    )

    base_to_front_right_wheel = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["-0.0619", "-0.13175", "0.107", "0", "0", "1.57", "base_link", "front_right_wheel"]
    )

    base_to_rear_left_wheel = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["-1.0", "0.13175", "0.107", "0", "0", "1.57", "base_link", "rear_left_wheel"]
    )

    base_to_rear_right_wheel = Node(
        package="tf2_ros",
        executable="static_transform_publisher",
        arguments=["-1.0", "-0.13175", "0.107", "0", "0", "1.57", "base_link", "rear_right_wheel"]
    )

    return LaunchDescription([
        ros_qwiic_servo,
        micro_ros_agent,
        cmdvel_to_servo,
        #torque_to_haptics, # uncomment if you want haptics all time
        wheel_odom,
        realsense2_camera,
        depth_to_laser_scan,
        rgbd_odometry,
        #rtabmap, # Uncomment for SLAM
        imu_filter,
        declare_model_path_cmd,
        robot_state_publisher,
        base_to_realsense,
        base_to_front_left_wheel,
        base_to_front_right_wheel,
        base_to_rear_left_wheel,
        base_to_rear_right_wheel,
        # Uncomment the following to run nav2
        # robot_localization,
        # declare_map_yaml_cmd,
        # declare_params_file_cmd,
        # ros2_navigation
    ])
