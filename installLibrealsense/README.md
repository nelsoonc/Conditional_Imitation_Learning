# installLibrealsense
These scripts install librealsense for Intel® RealSense™ cameras on Jetson TX2 Developer Kit

It is now possible on the NVIDIA Jetsons to do a simple install from a RealSense Debian repository (i.e. apt-get install). Previous versions of this repository require building librealsense from source, and rebuilding the Linux kernel (from my experience).

This is tested for L4T v32.6.1 (JetPack 4.6)

### buildLibrealsense.sh
To add librealsense python wrappers (pyrealsense2), you need to build librealsense from source. I didn't install librealsense demos and examples because I don't think those were needed for this project.
To build the librealsense library:
```
./buildLibrealsense.sh
```

Once the installaton is complete, you can try to access the camera from terminal:
```
realsense-viewer
```

To use pyrealsense2 on Python:
```
import pyrealsense2 as rs
```

## References
This information is derived from:
- https://github.com/jetsonhacks/installRealSenseSDK
- https://github.com/IntelRealSense/librealsense/blob/master/doc/installation.md
- https://github.com/IntelRealSense/librealsense/tree/master/wrappers/python


## Version Note
### September, 2021
- Intel® RealSense™ SDK 2.0 (v2.49.0)
- Jetson TX2, L4T v32.6.1, JetPack 4.6
