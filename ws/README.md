# Glide Simulation Workspace

## Setup
Install the following packages:
```
sudo apt install ros-foxy-navigation2 ros-foxy-nav2-bringup ros-foxy-joint-state-publisher-gui ros-foxy-xacro ros-foxy-gazebo-ros-pkgs ros-foxy-gazebo-ros ros-foxy-gazebo-plugins gazebo11 ros-foxy-rviz2 ros-foxy-robot-localization ros-foxy-depthimage-to-laserscan ros-foxy-libg2o python3-colcon-common-extensions
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

## Simulation Examples
To view the urdf run:
```
ros2 launch glide_robot vis_urdf.launch.py
```

To navigate the robot to a goal location run:
```
./run_sim.sh
```
The script will launch RViz and Gazebo environment. In RViz, click "Navigation2 Goal" and select a goal position and orientation in the map. The robot will then navigate to the selected goal. 


## Glide Demo
SSH into Glide and run the docker container:
```bash
ssh jetbot@IP_ADDRESS
cd repos/Glide
./run.sh
```
Connect to the docker container in a separate screen:
```bash
cd repos/Glide
./connect.sh
```

Launch the sensor and odometry nodes:
```bash
cd Glide/ws
source install/setup.bash
ros2 launch glide glide.launch.py
```

On your local machine launch the robot localization node and nav2:
```
ros2 launch glide_robot real_navigate.launch.py
```
Wait until you see `Activating bt_navigator`, `Activating waypoint_follower` and `Managed nodes are active` in the outputted log. Then launch `rviz`:
```bash
ros2 run rviz2 rviz2 -d ~/Glide/ws/src/glide_robot/rviz/nav2_config.rviz
```
When you see the robot and the costmaps appear in `rviz` you can start running demo. To demo Mode 1 (point-to-point navigation) run:
```bash
python3 mode1.py --traj_file experiment_A.json
```
To demo Mode 2 (shared control mode), run:
```bash
python3 mode2.py
```