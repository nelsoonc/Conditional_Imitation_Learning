#!/bin/bash
# Script: install Code OSS on Jetson TX2
# author: nelsoonc
# Bandung Institute of Technology, Mechanical Engineering 2017

# Reference : https://github.com/toolboc/vscode/releases

cd $HOME/Downloads
wget https://github.com/toolboc/vscode/releases/download/1.32.3/code-oss_1.32.3-arm64.deb
sudo apt install ./code-oss_1.32.3-arm64.deb

if [ $? -eq 0 ] ; then
  echo ""
  echo "Installation successful !"
  echo "execute 'code-oss' on terminal to open Code OSS"
else
  echo "There was an issue with the installation"
  echo "Please fix issues and retry install"
  exit 1
fi

echo ""
echo "You can manually remove the download file in Downloads directory if you want"