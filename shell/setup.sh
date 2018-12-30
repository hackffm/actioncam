#!/bin/bash
sudo apt update && sudo apt dist-upgrade
sudo apt autoremove && sudo apt autoclean
sudo apt install -y python3-venv opencv*
sudo apt install -y build-essential cmake pkg-config
sudo apt install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install -y libxvidcore-dev libx264-dev
sudo apt install -y libgtk2.0-dev libgtk-3-dev
sudo apt install -y libatlas-base-dev gfortran
sudo apt install -y python2.7-dev python3-dev
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
# thanks to adrian https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
if [ ! -d ~/opencv.tar.gz ]; then
	cd ~
	wget -O opencv.tar.gz https://github.com/opencv/opencv/archive/4.0.0.tar.gz
	wget -O opencv_contrip.tar.gz https://github.com/opencv/opencv_contrib/archive/4.0.0.tar.gz
	tar -xvf opencv.tar.gz
       	tar -xvf opencv_contrip.tar.gz
fi
