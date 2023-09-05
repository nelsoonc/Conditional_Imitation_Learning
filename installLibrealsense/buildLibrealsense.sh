#!/bin/bash
# Script: build librealsense and pyrealsense2 from source
# This script is for librealsense v2.49.0, Python3.6
# author: nelsoonc
# Bandung Institute of Technology, Mechanical Engineering 2017

LIBREALSENSE_DIRECTORY=${HOME}/librealsense
DOWNLOADS_DIRECTORY=${HOME}/Downloads

red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

# Install dependencies used for building librealsense
cd $PWD
sudo ./scripts/installDependencies.sh

# Use 'help read' to see more options in read command
echo ""
echo "Please make sure that no Realsense cameras are currently attached to Jetson"
echo ""
read -n 1 -s -r -p "Press any key to continue"
echo ""

# Retrieve librealsense source code to your local drive
if [ ! -d $LIBREALSENSE_DIRECTORY ] ; then
  cd $DOWNLOADS_DIRECTORY
  if [ ! -e $DOWNLOADS_DIRECTORY/librealsense.zip ] ; then
    echo "=== Retrieve librealsense source code ==="
    wget -O librealsense.zip https://github.com/IntelRealSense/librealsense/archive/refs/tags/v2.49.0.zip
  fi
  echo "Unzipping librealsense.."
  unzip -q librealsense.zip -d ${HOME}
  echo "Done"
  # Rename folder <path-to-original-name> <path-to-target-name>
  cd ${HOME}
  mv librealsense-2.49.0 librealsense
fi

cd $LIBREALSENSE_DIRECTORY
mkdir build
cd build

echo "=== Building librealsense and its python wrappers ==="
cmake ../ -DCMAKE_BUILD_TYPE=release \
    -DBUILD_PYTHON_BINDINGS:bool=ON \
    -DBUILD_WITH_CUDA=ON \
    -DBUILD_EXAMPLES=OFF \
    -DBUILD_GRAPHICAL_EXAMPLES=OFF \
    -DPYTHON_EXECUTABLE=/usr/bin/python3

# Check if CMake configuration successful
if [ $? -eq 0 ] ; then
  echo "${green}CMake configuration make successful${reset}"
else
  # Print message on stderr
  echo "${red}CMake issues${reset}" >&2
  echo "Please check the configuration being used"
  exit 1
fi

make -j4
if [ $? -eq 0 ] ; then
    echo "${green}Librealsense make successful${reset}"
else
  # Print message on stderr
  echo "${red}Librealsense make did not build${reset}" >&2
  echo "Retrying ..."
  # Try to build single thread
  make
  if [ $? -eq 0 ] ; then
    echo "${green}Librealsense make successful${reset}"
  else
    echo "${red}Librealsense did not build successfully${reset}"
    echo "Please fix issues and retry build"
    exit 1
  fi
fi

echo ""
echo "=== Installing librealsense ==="
sudo make install
if [ $? -eq 0 ] ; then
  echo ""
  echo "${green}Install successful !${reset}"
else
  echo "${red}There was an issue with the final installation${reset}"
  echo "Please fix issues and retry install"
  exit 1
fi

# Update PYTHONPATH environment variable to add the path to the pyrealsense library
# Check if it is already exist
if grep -Fxq 'export PYTHONPATH=$PYTHONPATH:/usr/local/lib' ~/.bashrc ; then
  echo 'export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.6/pyrealsense2' >> ~/.bashrc
  echo "PYTHONPATH added to ~/.bashrc. Python wrapper is now available for importing pyrealsense2"
  echo "Check 'sudo gedit ~/.bashrc' to see your system environment path"
else
  echo 'export PYTHONPATH=$PYTHONPATH:/usr/local/lib' >> ~/.bashrc
  echo 'export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python3.6/pyrealsense2' >> ~/.bashrc
  echo "PYTHONPATH added to ~/.bashrc. Python wrapper is now available for importing pyrealsense2"
  echo "Check 'sudo gedit ~/.bashrc' to see your system environment path"
fi
source ~/.bashrc

cd $LIBREALSENSE_DIRECTORY
echo ""
echo "Applying udev rules"
# Copy udev rules from official folder so that camera can be run from user space
sudo cp config/99-realsense-libusb.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && udevadm trigger

echo ""
echo "${green}Librealsense library installed successfully${reset}"
echo "The library is installed in /usr/local/lib"
echo "------------------------------------------"
echo ""