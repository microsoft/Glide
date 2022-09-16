# Adapted from fhttps://automaticaddison.com

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

  # Set the path to different files and folders.
  pkg_share = FindPackageShare(package='glide').find('glide')
  default_launch_dir = os.path.join(pkg_share, 'launch')
  default_model_path = os.path.join(pkg_share, 'models/glide_description.urdf')
  robot_localization_file_path = os.path.join(pkg_share, 'config/ekf.yaml') 
  robot_name_in_urdf = 'glide_bot'
  default_rviz_config_path = os.path.join(pkg_share, 'rviz/nav2_config.rviz')
  nav2_dir = FindPackageShare(package='nav2_bringup').find('nav2_bringup') 
  nav2_launch_dir = os.path.join(nav2_dir, 'launch') 
  static_map_path = os.path.join(pkg_share, 'maps', '99_hallway_study_final.yaml')
  nav2_params_path = os.path.join(pkg_share, 'params', 'nav2_params.yaml')
  nav2_bt_path = FindPackageShare(package='nav2_bt_navigator').find('nav2_bt_navigator')
  behavior_tree_xml_path = os.path.join(nav2_bt_path, 'behavior_trees', 'navigate_w_replanning_and_recovery.xml')
  
  # Launch configuration variables specific to simulation
  autostart = LaunchConfiguration('autostart')
  default_bt_xml_filename = LaunchConfiguration('default_bt_xml_filename')
  map_yaml_file = LaunchConfiguration('map')
  model = LaunchConfiguration('model')
  namespace = LaunchConfiguration('namespace')
  params_file = LaunchConfiguration('params_file')
  rviz_config_file = LaunchConfiguration('rviz_config_file')
  slam = LaunchConfiguration('slam')
  use_namespace = LaunchConfiguration('use_namespace')
  use_rviz = LaunchConfiguration('use_rviz')
  
  remappings = [('/tf', 'tf'),
                ('/tf_static', 'tf_static')]
  
  # Declare the launch arguments  
  declare_namespace_cmd = DeclareLaunchArgument(
    name='namespace',
    default_value='',
    description='Top-level namespace')

  declare_use_namespace_cmd = DeclareLaunchArgument(
    name='use_namespace',
    default_value='False',
    description='Whether to apply a namespace to the navigation stack')
        
  declare_autostart_cmd = DeclareLaunchArgument(
    name='autostart', 
    default_value='true',
    description='Automatically startup the nav2 stack')

  declare_bt_xml_cmd = DeclareLaunchArgument(
    name='default_bt_xml_filename',
    default_value=behavior_tree_xml_path,
    description='Full path to the behavior tree xml file to use')
        
  declare_map_yaml_cmd = DeclareLaunchArgument(
    name='map',
    default_value=static_map_path,
    description='Full path to map file to load')
        
  declare_model_path_cmd = DeclareLaunchArgument(
    name='model', 
    default_value=default_model_path, 
    description='Absolute path to robot urdf file')
    
  declare_params_file_cmd = DeclareLaunchArgument(
    name='params_file',
    default_value=nav2_params_path,
    description='Full path to the ROS2 parameters file to use for all launched nodes')
    
  declare_rviz_config_file_cmd = DeclareLaunchArgument(
    name='rviz_config_file',
    default_value=default_rviz_config_path,
    description='Full path to the RVIZ config file to use')

  declare_slam_cmd = DeclareLaunchArgument(
    name='slam',
    default_value='False',
    description='Whether to run SLAM')

  # Better to launch rviz separately in case it crashes and you need to restart it. Set to True if you want to launch rviz in this launch file.
  declare_use_rviz_cmd = DeclareLaunchArgument(
    name='use_rviz',
    default_value='False',
    description='Whether to start RVIZ')

  # Specify the actions

  # Start robot localization using an Extended Kalman filter
  start_robot_localization_cmd = Node(
    package='robot_localization',
    executable='ekf_node',
    name='ekf_filter_node',
    output='screen',
    parameters=[robot_localization_file_path, 
    {'use_sim_time': 'False'}])

  # Launch RViz
  start_rviz_cmd = Node(
    condition=IfCondition(use_rviz),
    package='rviz2',
    executable='rviz2',
    name='rviz2',
    output='screen',
    arguments=['-d', rviz_config_file])    

  param_config = os.path.join(get_package_share_directory('depthimage_to_laserscan'), 'cfg', 'param.yaml')
  depth_to_laser_scan_cmd = Node(
    package='depthimage_to_laserscan',
    executable='depthimage_to_laserscan_node',
    name='depthimage_to_laserscan_node',
    remappings=[('depth','/depth/image_rect_raw'),
                ('depth_camera_info', '/depth/camera_info')],
    parameters=[param_config]
  )

  # Launch the ROS 2 Navigation Stack
  start_ros2_navigation_cmd = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(os.path.join(nav2_launch_dir, 'bringup_launch.py')),
    launch_arguments = {'namespace': namespace,
                        'use_namespace': use_namespace,
                        'slam': slam,
                        'map': map_yaml_file,
                        'use_sim_time': 'False',
                        'params_file': params_file,
                        'default_bt_xml_filename': default_bt_xml_filename,
                        'autostart': autostart}.items())

  parameters=[{
        'frame_id':'base_footprint',
        'subscribe_depth':True,
      #   'subscribe_rgbd': True,
        'imu_topic':'/camera/imu/sample',
        'wait_imu_to_init': True,
        'subscribe_scan': True,
        'approx_sync':False,
      #   "fill_holes_size": 2,
        "visual_odometry":True,
        "publish_null_when_lost": False,
        "Odom/ResetCountdown": "1"}]

  remappings=[
        ('rgb/image', '/camera/color/image_raw'),
        ('imu', '/imu/data'),
      #   ('rgbd/image', "/camera/aligned_depth_to_color/image_raw")
        ('rgb/camera_info', '/camera/color/camera_info'),
        ('depth/image', '/camera/aligned_depth_to_color/image_raw')]

  rgbd_odometry = Node(
      package='rtabmap_ros', executable='rgbd_odometry', output='screen',
      parameters=parameters,
      remappings=remappings
  )

  # Create the launch description and populate
  ld = LaunchDescription()

  # Declare the launch options
  ld.add_action(declare_namespace_cmd)
  ld.add_action(declare_use_namespace_cmd)
  ld.add_action(declare_autostart_cmd)
  ld.add_action(declare_bt_xml_cmd)
  ld.add_action(declare_map_yaml_cmd)
  ld.add_action(declare_model_path_cmd)
  ld.add_action(declare_params_file_cmd)
  ld.add_action(declare_rviz_config_file_cmd)
  ld.add_action(declare_slam_cmd)
  ld.add_action(declare_use_rviz_cmd) 
  ld.add_action(start_robot_localization_cmd)
  ld.add_action(start_rviz_cmd)
  ld.add_action(start_ros2_navigation_cmd)
  
  return ld
