#!/bin/bash
# Script: bind Arduino under a static name
# author: nelsoonc
# Bandung Institute of Technology, Mechanical Engineering 2017

# Reference: https://unix.stackexchange.com/questions/66901/how-to-bind-usb-device-under-a-static-name
# Reference: https://www.arduino.cc/en/guide/linux#toc6

RULES_DIR=/etc/udev/rules.d/99-usb-serial.rules
# VARIABLE TO BE CONFIGURED
# udevadm info -a -p  $(udevadm info -q path -n /dev/ttyUSB0)
NAME=ArduinoNano
SUBSYSTEM=tty
idVendor=1a86
idProduct=7523
username=$whoami

# Allowing system to upload code to arduino
sudo usermode -a -G dialout $username

sudo sh -c "echo 'SUBSYSTEM==\"$SUBSYSTEM\", ATTRS{idVendor}==\"$idVendor\", ATTRS{idProduct}==\"$idProduct\", SYMLINK+=\"$NAME\"' >> $RULES_DIR"
sudo udevadm trigger
sleep 2
if [ -e /dev/$NAME ] ; then
  echo "Done binding your Arduino under a static name"
  echo "Use ls /dev to check your Arduino name, it should be: ${NAME}"
else
  echo "Something's wrong"
  echo "Try to check the issues"
fi