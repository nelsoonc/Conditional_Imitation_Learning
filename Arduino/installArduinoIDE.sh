#!/bin/bash
# Script: install Arduino IDE  on Jetson TX2
# author: nelsoonc
# Bandung Institute of Technology, Mechanical Engineering 2017

VERSION=1.8.16
ARDUINO_DIR=$HOME/arduino-${VERSION}
DOWNLOADS_DIRECTORY=$HOME/Downloads

if [ ! -d $ARDUINO_DIR ] ; then
  if [ ! -e $DOWNLOADS_DIRECTORY/arduino-$VERSION.tar.xz ] ; then
    cd $DOWNLOADS_DIRECTORY
    echo "=== Retrieve Arduino IDE source ==="
    wget -O arduino-$VERSION.tar.xz wget https://downloads.arduino.cc/arduino-1.8.16-linuxaarch64.tar.xz
  fi
  echo "Extracting Arduino.."
  tar -xf arduino-$VERSION.tar.xz -C $HOME
  echo "Done"
fi

# Install Arduino IDE
cd $ARDUINO_DIR
./install.sh

if [ $? -eq 0 ] ; then
  echo ""
  echo "Arduino IDE installation successful !"
else
  echo "There was an issue with the installation"
  echo "Please fix issues and retry install"
  exit 1
fi

echo ""
echo "You can manually remove the download file in home and Downloads directory if you want"