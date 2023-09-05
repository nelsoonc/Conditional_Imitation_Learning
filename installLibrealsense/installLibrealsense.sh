#!/bin/bash
# Script for install librealsense from debian package
# author: nelsoonc
# Bandung Institute of Technology, Mechanical Engineering 2017

# reference : https://github.com/IntelRealSense/librealsense/blob/master/doc/installation_jetson.md
# Register the server's public key:
sudo apt-key adv --keyserver keyserver.ubuntu.com  --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key

# Add the server to the list of repositories:
sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main" -u

# Install the SDK
sudo apt-get install apt-utils -y
sudo apt-get install librealsense2-utils librealsense2-dev -y