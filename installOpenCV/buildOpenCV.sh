#!/bin/bash
# Script: build OpenCV v4.5.3 from source
# author : nelsoonc
# Bandung Institute of Technology, Mechanical Engineering 2017

# Reference: https://github.com/jetsonhacks/buildOpenCVTX2

VERSION=4.5.3
OPENCV_DIRECTORY=${HOME}/opencv
OPENCV_CONTRIB=${HOME}/opencv_contrib/modules
CMAKE_INSTALL_PREFIX=/usr/local
DOWNLOADS_DIRECTORY=${HOME}/Downloads
THIS_SCRIPT_DIR=$PWD
ARCH_BIN=6.2 # https://study.marearts.com/2021/06/cudaarchbin-table-for-gpu-type.html


red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

# Install dependencies used for building OpenCV
cd $PWD
sudo ./scripts/installDependencies.sh

# https://devtalk.nvidia.com/default/topic/1007290/jetson-tx2/building-opencv-with-opengl-support-/post/5141945/#5141945
echo "Patch cuda_gl_interop.h"
cd /usr/local/cuda/include
sudo patch -N cuda_gl_interop.h ${THIS_SCRIPT_DIR}'/patches/OpenGLHeader.patch'
# Clean up the OpenGL tegra libs that usually get crushed
cd /usr/lib/aarch64-linux-gnu/
sudo ln -sf libGL.so.1.0.0 libGL.so

# Cloning official librealsense repository to your local drive
if [ ! -d $OPENCV_DIRECTORY ] ; then
  if [ ! -e $DOWNLOADS_DIRECTORY/opencv.zip ] ; then
    cd ${DOWNLOADS_DIRECTORY}
    echo "=== Retrieve OpenCV source code ==="
    wget -O opencv.zip https://github.com/opencv/opencv/archive/refs/tags/$VERSION.zip
    wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/refs/tags/$VERSION.zip
  fi
  echo "Unzipping OpenCV.."
  unzip -q opencv.zip -d ${HOME}
  unzip -q opencv_contrib.zip -d ${HOME}
  echo "Done"
  # Rename folder <path-to-original-name> <path-to-target-name>
  cd ${HOME}
  mv opencv-$VERSION opencv
  mv opencv_contrib-$VERSION opencv_contrib
fi

cd $OPENCV_DIRECTORY
mkdir build
cd build

# Here are some options to install source examples and tests
#     -D INSTALL_TESTS=ON \
#     -D OPENCV_TEST_DATA_PATH=../opencv_extra/testdata \
#     -D INSTALL_C_EXAMPLES=ON \
#     -D INSTALL_PYTHON_EXAMPLES=ON \
# There are also switches which tell CMAKE to build the samples and tests
# Check OpenCV documentation for details

echo ""
echo ""
echo "This whole process will take time ~1.5 hours. Please kindly wait"
sleep 3 # Sleep for 3 seconds
echo "=== Building OpenCV library from source ==="
time cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX} \
      -D WITH_CUDA=ON \
      -D CUDA_ARCH_BIN=${ARCH_BIN} \
      -D CUDA_ARCH_PTX="" \
      -D OPENCV_EXTRA_MODULES_PATH=${OPENCV_CONTRIB} \
      -D BUILD_EXAMPLE=OFF \
      -D INSTALL_C_EXAMPLES=OFF \
      -D INSTALL_PYTHON_EXAMPLES=OFF \
      -D ENABLE_FAST_MATH=ON \
      -D CUDA_FAST_MATH=ON \
      -D WITH_CUBLAS=ON \
      -D WITH_LIBV4L=ON \
      -D WITH_GSTREAMER=OFF \
      -D WITH_QT=OFF \
      -D WITH_OPENGL=ON \
      -D BUILD_LIST=core,cudev,dnn,flann,gapi,highgui,imgcodecs,imgproc,ml,objdetect,python3,video,videoio \
      ../
# More modules: https://github.com/opencv/opencv/tree/master/modules


# Check if CMake configuration successful
if [ $? -eq 0 ] ; then
  echo "${green}CMake configuration make successful${reset}"
  echo ""
else
  # Print message on stderr
  echo "${red}Error: CMake issues${reset}" >&2
  echo "Please check the configuration being used"
  exit 1
fi

make -j4
if [ $? -eq 0 ] ; then
    echo "${green}OpenCV make successful${green}"
else
  # Print message on stderr
  echo "${red}OpenCV make did not build${reset}" >&2
  echo "Retrying ..."
  # Try to build single thread
  make
  if [ $? -eq 0 ]; then
    echo "${green}OpenCV make successful${reset}"
  else
    echo "${red}OpenCV did not build successfully${reset}" >&2
    echo "Please fix issues and retry build"
    exit 1
  fi
fi

echo ""
echo ""
echo "=== Installing OpenCV ==="
sudo make install
if [ $? -eq 0 ] ; then
  echo ""
  echo "${green}Install successful !${reset}"
  echo "OpenCV installed in: $CMAKE_INSTALL_PREFIX"
else
  echo "${red}There was an issue with the final installation${reset}"
  echo "Please fix issues and retry install"
  exit 1
fi