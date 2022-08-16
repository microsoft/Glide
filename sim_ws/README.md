# Glide Simulation Workspace

## Setup
Install the following packages:
```
sudo apt install ros-foxy-navigation2 ros-foxy-nav2-bringup ros-foxy-joint-state-publisher-gui ros-foxy-xacro ros-foxy-gazebo-ros-pkgs ros-foxy-gazebo-ros ros-foxy-gazebo-plugins gazebo11 ros-foxy-rviz2 ros-foxy-robot-localization ros-foxy-depthimage-to-laserscan ros-foxy-libg2o
```

Build the workspace:
```bash
cd Glide/
git submodule init
git submodule update
cd sim_ws/
colcon build
source install/setup.bash
```

## Examples
To view the urdf run:
```
ros2 launch glide_robot vis_urdf.launch.py
```

To navigate the robot to a goal location run:
```
./run_sim.sh
```
The script will launch RViz and Gazebo environment. In RViz, click "Navigation2 Goal" and select a goal position and orientation in the map. The robot will then navigate to the selected goal. 