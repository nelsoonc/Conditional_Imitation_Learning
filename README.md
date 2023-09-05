# Conditional Imitation Learning on Radio Controlled Car

<img src="https://github.com/nelsoonc/file_references/blob/main/CIL/Final%20System.jpg" title="Conditional Imitation Learning" height="360"/>

This is full repository to "Implementation of Conditional Imitation Learning on Autonomous Driving System".

These are the hardwares I used in this project:
1. U.S. 4x4 Military Vehicle | HG-P408 | 1/10-Scale Radio Controlled Car
2. Intel® RealSense™ Depth Camera D435i
3. NVIDIA Jetson TX2 Developer Kit
4. Arduino Nano
5. Adafruit PCA9685

You can clone this repository to your local machine
```
git clone https://github.com/nelsoonc/Conditional_Imitation_Learning.git
```

### installLibrealsense
Librealsense is a cross-platform library (Linux, OSX, Windows) for capturing data from the Intel® RealSense™ Camera, such as D435i. This folder contains scripts to build the librealsense library and its Python wrapper, so you can access realsense library with Python.

https://github.com/IntelRealSense/librealsense

### installOpenCV
OpenCV is a library of programming functions mainly aimed at real-time computer vision (CV). This folder contains scripts to build OpenCV library from source on Jetson TX2.

https://github.com/opencv/opencv

### installTensorFlow
TensorFlow is a free and open-source software library for machine learning and artificial intelligence. NVIDIA has provided TensorFlow for JetPack, so we can follow NVIDIA's instructions to install TensorFlow on Jetson.
