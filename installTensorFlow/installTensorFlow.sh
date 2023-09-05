#!/bin/bash
# Script: install TensorFlow 2.5.0 on Jetson TX2, Jetpack v4.6
# Python3.6
# author: nelsoonc
# Bandung Institute of Technology, Mechanical Engineering 2017

# https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html

TF_VERSION=2.5.0
NV_VERSION=21.8

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

sudo apt-get update
echo "${green}Installing dependencies${reset}"
sudo apt-get install -y libhdf5-serial-dev \
    hdf5-tools \
    libhdf5-dev \
    zlib1g-dev \
    zip \
    libjpeg8-dev \
    liblapack-dev \
    libblas-dev \
    gfortran

# pip installation and package installation with pip
sudo apt-get install -y python3-pip
sudo pip3 install -U pip testresources setuptools==49.6.0
sudo pip3 install -U --no-deps numpy==1.19.4 \
    future==0.18.2 \
    mock==3.0.5 \
    keras_preprocessing==1.1.2 \
    keras_applications==1.0.8 \
    gast==0.4.0 \
    protobuf \
    pybind11 \
    cython \
    pkgconfig
sudo env H5PY_SETUP_REQUIRES=0 pip3 install -U h5py==3.1.0

# Install TensorFlow 2.5.0 for Jetpack v4.6
sudo pip3 install --pre --extra-index-url https://developer.download.nvidia.com/compute/redist/jp/v46 tensorflow==$TF_VERSION+nv$NV_VERSION

if [ $? -eq 0 ] ; then
  echo ""
  echo "${green}TensorFlow install is successful !${reset}"
else
  echo "${red}There was an issue with the installation${reset}"
  echo "Install was not successful"
  exit 1
fi