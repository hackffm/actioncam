if [ ! -d ~/temp ]; then
    mkdir ~/temp
fi
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-armv7l.sh -P ~/temp
chmod u+x ~/temp/Miniconda3-latest-Linux-arm71.sh
~temp/Miniconda3-latest-Linux-arm71.sh -b -p ~/miniconda
