#!/bin/bash
# Script: install Visual Studio Code on Jetson TX2
# author: nelsoonc
# Bandung Institute of Technology, Mechanical Engineering 2017

# Reference : https://github.com/JetsonHacksNano/installVSCode
# To build from source: https://github.com/zenetio/Install-VScode-On-TX2

cd $HOME/Downloads
wget -N -O vscode-linux-deb.arm64.deb https://update.code.visualstudio.com/latest/linux-deb-arm64/stable
sudo apt install ./vscode-linux-deb.arm64.deb

if [ $? -eq 0 ] ; then
  echo ""
  echo "Installation successful !"
  echo "execute 'code' on terminal to open Visual Studio Code"
else
  echo "There was an issue with the installation"
  echo "Please fix issues and retry install"
  exit 1
fi

echo ""
echo "You can manually remove the download file in Downloads directory if you want"