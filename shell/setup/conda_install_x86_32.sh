if [ ! -d ~/temp ]; then
    mkdir ~/temp
fi
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86.sh ~/temp
chmod u+x Miniconda3-latest-Linux-x86.sh
./Miniconda3-latest-Linux-x86.sh -b -p /home/pi/miniconda
