#!/bin/bash
echo
echo "Building Micro ROS"
echo
cd /ws/src/microros_ws
rosdep install --from-path src --ignore-src -y
colcon build
source install/local_setup.bash
ros2 run micro_ros_setup create_agent_ws.sh
ros2 run micro_ros_setup build_agent.sh
source install/local_setup.bash

echo
echo "Building remaining packages"
echo
cd /ws/src
colcon build

echo
echo "Rebuilding packages to handle "
echo
colcon build
source install/local_setup.bash

