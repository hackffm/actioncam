echo 'set venv'
actioncam_dir='/home/pi/git/actioncam/'
source $actioncam_dir'venv/bin/activate'

echon 'build opencv 4.0'
cd ~/opencv-4.0.0/
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-4.0.0/modules \
      -D ENABLE_NEON=ON \
      -D ENABLE_VFPV3=ON \
      -D BUILD_TESTS=OFF \
      -D OPENCV_ENABLE_NONFREE=ON \
      -D INSTALL_PYTHON_EXAMPLES=OFF \
      -D VTK_DIR \
      -D BUILD_opencv_python3=yes \
      -D BUILD_EXAMPLES=OFF ..
