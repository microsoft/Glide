export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$PWD/src/glide_robot/models/
source install/setup.bash
ros2 launch glide_robot sim_navigate.launch.py
