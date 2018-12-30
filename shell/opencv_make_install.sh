CONF_SWAPSIZE=1024
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
#number of processors on a pi zero is two !
cd ~/opencv-4.0.0/build
make -j2
sudo make install
sudo ldconfig

