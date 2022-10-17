#!/bin/bash
echo
echo "Building Micro ROS"
echo
cd /ws/src/microros_ws
rosdep install --from-path src --ignore-src -y
colcon build --symlink-install --event-handlers console_cohesion+ --base-paths /ws --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
source install/local_setup.bash
ros2 run micro_ros_setup create_agent_ws.sh
ros2 run micro_ros_setup build_agent.sh
source install/local_setup.bash

echo
echo "Building remaining packages"
echo
colcon build --symlink-install --event-handlers console_cohesion+ --base-paths /ws --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo
source install/local_setup.bash

