# installOpenCV
These scripts build OpenCV for the NVIDIA Jetson TX2 Development Kit. OpenCV library that comes with JetPack does not support CUDA processing. So, building OpenCV from source is almost recommended for your projects.
Reference: https://forums.developer.nvidia.com/t/jetson-nano-cuda-cudnn-opencv/169731

### buildOpenCV.sh
This script will build OpenCV from source and install it on the system.
```
./buildOpenCV.sh
```
Once the installation is complete, you can check your OpenCV version and its build information
```
python3
import cv2
cv.__version__
print(cv2.getBuildInformation())
```

### removeOpenCVSource.sh
The folder ~/opencv and ~/opencv_contrib contain the source, build and extra data files. You can remove them and save some disk spaces since you don't need them to run OpenCV. If you wish to remove them after the installation, a convenience script is provided:
```
./removeOpenCVSource.sh
```

## References
This information is derived from:
https://github.com/jetsonhacks/buildOpenCVTX2

## Version Notes
### September, 2021
- OpenCV 4.5.3
- JetPack 4.6, L4T v32.6.1, CUDA 10.2
- Python 3.6.9

### October, 2021
- OpenCV 4.5.4
