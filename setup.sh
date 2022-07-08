#!/bin/bash

mkdir -p ws/src
vcs import --recursive --input glide.repos ws/src

echo
echo
echo "To Run:"
echo "./run.sh"
echo
echo "In another console:"
echo "./connect.sh"
echo "/ws/src/build_src.sh"
echo
echo "To start glide:"
echo "ros2 launch glide glide.launch.py"
echo
