#!/bin/bash
sudo apt update && sudo apt dist-upgrade
sudo apt autoremove && sudo apt autoclean
sudo apt install -y python3-venv
sudo apt install -y build-essential cmake unzip pkg-config
sudo apt install -y libjpeg-dev libtiff-dev libjasper-dev libpng-dev
sudo apt install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt install -y libxvidcore-dev libx264-dev
sudo apt install -y libgtk-3-dev libcanberra-gtk*
sudo apt install -y libatlas-base-dev gfortran
sudo apt install -y python3-dev
python3 -m pip install --upgrade pip
if [ ! -d ~/actioncam ]; then
	mkdir ~/actioncam
fi
