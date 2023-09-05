#!/bin/bash
# Script: install OpenCV dependencies on Jetson TX2
# author : nelsoonc
# Bandung Institute of Technology, Mechanical Engineering 2017

green=`tput setaf 2`
reset=`tput sgr0`

echo "${green}Update and upgrade ubuntu packages${reset}"
sudo apt-get update
sudo apt-get upgrade

# Install dependencies used in the desired configuration
cd ${HOME}
echo "${green}Installing build dependencies${reset}"
sudo apt-get install -y \
    build-essential \
    cmake \
    wget \
    zip \
    tar \
    gfortran \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libavresample-dev \
    libavutil-dev \
    libdc1394-22-dev \
    libeigen3-dev \
    libgflags-dev \
    libgoogle-glog-dev \
    libglew-dev \
    libgtk2.0-dev \
    libgtk-3-dev \
    libgtkglext1-dev \
    libjpeg-dev \
    liblapack-dev \
    liblapacke-dev \
    libopenblas-dev \
    libpng-dev \
    libpostproc-dev \
    libswscale-dev \
    libtbb-dev \
    libtiff-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    qt5-default \
    qtbase5-dev \
    qtdeclarative5-dev \
    zlib1g-dev \
    pkg-config \
    python3-dev \
    python3-numpy