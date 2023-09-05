#!/bin/bash
# Script: remove all OpenCV sources
# author: nelsoonc
# Bandung Institute of Technology, Mechanical Engineering 2017

# Default installation is in the $HOME directory

OPENCV_SOURCE_DIR=$HOME
DOWNLOADS_DIR=$HOME/Downloads

echo "Removing OpenCV source code from $OPENCV_SOURCE_DIR"
cd $OPENCV_SOURCE_DIR

if [ -d "opencv" ] ; then
  echo "Removing opencv source"
  sudo rm -r opencv
else
  echo "Could not find opencv directory"
  echo "There is nothing to remove"
fi

if [ -d "opencv_contrib" ] ; then
  echo "Removing opencv_contrib source"
  sudo rm -r opencv_contrib
else
  echo "Could not find opencv_contrib directory"
  echo "There is nothing to remove"
fi

echo "Removing OpenCV source code from $OPENCV_SOURCE_DIR"
cd $DOWNLOADS_DIR

if [ -d "opencv.zip" ] ; then
  echo "Removing opencv source zip"
  sudo rm opencv.zip
else
  echo "Could not find opencv directory"
  echo "There is nothing to remove"
fi

if [ -d "opencv_contrib.zip" ] ; then
  echo "Removing opencv_contrib source zip"
  sudo rm opencv_contrib.zip
else
  echo "Could not find opencv_contrib directory"
  echo "There is nothing to remove"
fi

echo "Done removing all files"