export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$PWD/src/glide/models/
source install/setup.bash
ros2 launch glide sim_navigate.launch.py
