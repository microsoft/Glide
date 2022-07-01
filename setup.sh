#!/bin/bash

mkdir -p ws/src
vcs import --recursive --input jetbot.repos ws/src

cp build_src.sh ws/src/

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
echo "ros2 run glide glide.launch.py"
echo