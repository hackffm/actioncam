#!/bin/bash
sudo apt update && sudo apt dist-upgrade
sudo apt autoremove && sudo apt autoclean
sudo apt install -y python3-venv opencv*
sudo apt install -y build-essential cmake unzip pkg-config
sudo apt install -y libjpeg-dev libtiff-dev libjasper-dev libpng-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install -y libxvidcore-dev libx264-dev
sudo apt install -y libgtk-3-dev libcanberra-gtk*
sudo apt install -y libatlas-base-dev gfortran
sudo apt install -y python3-dev
python3 -m pip install --upgrade pip
if [ ! -d ../venv ]; then
	mkdir ../venv
	python3 -m venv ../venv
fi
echo 'set venv'
actioncam_dir='/home/pi/git/actioncam/'
source $actioncam_dir'venv/bin/activate'

if [ ! -d ../temp ]; then
	mkdir ../temp
fi
echo 'get opencv 4.0'
# thanks to adrian https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
if [ ! -f ~/opencv.zip ]; then
	cd ~
	wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip
	wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip
fi
cd ~
unzip opencv.zip
unzip opencv_contrib.zip
