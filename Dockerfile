FROM ros:foxy

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python-is-python3 \
        python3-pip \
	libopencv-dev \
	python3-opencv \
        libboost-all-dev \
        openssl \
        git \
        gdb \
	i2c-tools \
        libcurl4-openssl-dev \
        libssl-dev \
        curl \
        libi2c-dev \
        build-essential \
        ros-$ROS_DISTRO-realsense2-camera \
        ros-$ROS_DISTRO-realsense2-description \
        ros-$ROS_DISTRO-imu-tools \
        ros-$ROS_DISTRO-joint-state-publisher-gui \
        ros-$ROS_DISTRO-xacro

ENV WORKSPACE_ROOT=/ws
RUN echo 'source /opt/ros/foxy/setup.bash' >> /root/.bashrc && \
    echo 'source /ws/src/install/local_setup.bash' >> /root/.bashrc

ENTRYPOINT ["./ros_entrypoint.sh"]
CMD [ "bash" ]
