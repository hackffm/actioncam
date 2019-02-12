#!/bin/bash
DEBIAN_FRONTEND=noninteractive
sudo apt update && sudo apt --yes dist-upgrade
sudo apt --yes install  python3-venv
sudo apt --yes install  build-essential cmake unzip pkg-config
sudo apt --yes install  libjpeg-dev libtiff-dev libjasper-dev libpng-dev
sudo apt --yes install  libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt --yes install  libxvidcore-dev libx264-dev
sudo apt --yes install  libgtk-3-dev libcanberra-gtk*
sudo apt --yes install  libatlas-base-dev gfortran
sudo apt --yes install  python3-dev
sudo apt --yes install libgstreamer-plugins-base1.0-dev
sudo apt --yes install libgflags* python3-gflags python-gflags python3-google*
sudo apt --yes install libgoogl* libeigen3* python3-minieigen
sudo apt autoremove && sudo apt autoclean
