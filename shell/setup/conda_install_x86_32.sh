if [ ! -d ~/temp ]; then
    mkdir ~/temp
fi
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86.sh -P ~/temp
chmod u+x ~/temp/Miniconda3-latest-Linux-x86.sh
~/temp/Miniconda3-latest-Linux-x86.sh -b -p /home/pi/miniconda
