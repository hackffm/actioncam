#!/bin/bash
if [ "$(id -u)" -ne 0 ]; then
        echo 'This script must be run by root' >&2
        exit 1
fi
echo install debian packages
export DEBIAN_FRONTEND=noninteractive
apt update && apt --yes dist-upgrade
# apt install --yes libatlas3-base libwebp6 libtiff5 libjasper1 libilmbase23 libopenexr23 
# apt install --yes libgstreamer1.0-0 libavcodec58 libavformat58 libavutil56
# apt install --yes libswscale5 libgtk-3-0 libpangocairo-1.0-0 libpango-1.0-0 libatk1.0-0 
# apt install --yes libcairo-gobject2 libcairo2 libgdk-pixbuf2.0-0
# apt install --yes libsz2 libharfbuzz0b
# apt install --yes libqtgui4 libqt4-test libqtcore4
apt install --yes libgslcblas0 libhdf5-dev libhdf5-serial-dev # libatlas-base-dev libjasper-dev 
apt install --yes python3-opencv python3-cv-bridge libopencv-dev
apt install --yes build-essential cmake pkg-config # libgtk-3-dev "libcanberra-gtk*"
apt install --yes libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev
apt install --yes libjpeg-dev libpng-dev libtiff-dev gfortran openexr opencl-headers
apt install --yes python3-dev python3-numpy libtbbmalloc2 libtbb-dev # libdc1394-22-dev
apt install --yes python3-venv python3-pip
