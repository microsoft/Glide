#!/bin/bash
# To clone the Glide repo:
# git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager-core.exe"
# git clone https://github.com/microsoft/Glide.git



sudo apt update
sudo apt upgrade

# Installing ROS2
sudo apt update && sudo apt install curl gnupg2 lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt upgrade
sudo apt install ros-foxy-desktop
sudo apt install ros-foxy-navigation2 ros-foxy-nav2-bringup ros-foxy-joint-state-publisher-gui ros-foxy-xacro ros-foxy-gazebo-ros-pkgs ros-foxy-gazebo-ros ros-foxy-gazebo-plugins gazebo11 ros-foxy-rviz2 ros-foxy-robot-localization ros-foxy-depthimage-to-laserscan ros-foxy-libg2o python3-colcon-common-extensions
