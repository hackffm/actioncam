echo 'get opencv 4.0'
# thanks to adrian https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
if [ ! -f ~/opencv.zip ]; then
	cd ~
	wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip
	wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip
fi
if [ ! -f ~/opencv_contrib.zip ]; then
	cd ~
	wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip
fi
cd ~
unzip opencv.zip
unzip opencv_contrib.zip