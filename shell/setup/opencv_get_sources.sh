echo 'get opencv 4.0'
# thanks to adrian https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/
if [ ! -f ~/opencv.zip ]; then
	cd ~
	wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.1.zip
	wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.1.zip
fi
if [ ! -f ~/opencv_contrib.zip ]; then
	cd ~
	wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.1.zip
fi
echo 'unzip opencv'
cd ~
unzip opencv.zip
unzip opencv_contrib.zip
if [ -f ~/opencv.zip ]; then
	echo 'remove zip files'
	rm opencv.zip
fi
if [ -f ~/opencv_contrib.zip ]; then
	rm ~/opencv_contrib.zip
fi
echo 'rename opencv folder'
mv ~/opencv-4.0.1 ~/opencv
mv ~/opencv_contrib-4.0.1 ~/opencv_contrib
