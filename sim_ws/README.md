# Glide Simulation Workspace

## Setup
Install the following packages:
```
sudo apt install ros-foxy-navigation2 ros-foxy-nav2-bringup ros-foxy-joint-state-publisher-gui ros-foxy-xacro ros-foxy-gazebo-ros-pkgs ros-foxy-gazebo-ros ros-foxy-gazebo-plugins gazebo11 ros-foxy-rviz2 ros-foxy-robot-localization ros-foxy-depthimage-to-laserscan ros-foxy-libg2o
```

Build the workspace:
```bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:<path-to>/Glide/sim_ws/src/glide_robot/models/
cd Glide/sim_ws/
colcon build
source install/setup.bash
```

## Examples
To view the urdf run:
```
ros2 launch glide_robot vis_urdf.launch.py
```

Update `hwlabcorridor.world` in the `worlds` folder to include the correct path the the mesh.

To navigate the robot to a goal location run:
```
ros2 launch glide_robot navigate.launch.py
```
The script will launch RViz and Gazebo environment. In RViz, click "Navigation2 Goal" and select a goal position and orientation in the map. The robot will then navigate to the selected goal. 