#!/bin/bash
echo "check setup"
if [ ! -d ~/actioncam ]; then
  echo "create actioncam folders"
	mkdir ~/actioncam
	mkdir ~/actioncam/data
	mkdir ~/actioncam/compressed
	mkdir ~/actioncam/log
	mkdir ~/actioncam/recordings
fi
#
if [ ! -f ~/actioncam/config.json ]; then
  	echo "prepare config"
    cp config.json ~/actioncam
    sed -i -e 's/pi/'"${USER}"'/g' ~/actioncam/config.json
fi
#
if [ ! -d ~/actioncam/venv ]; then
  mkdir ~/actioncam/venv
  echo create python venv
  python3 -m venv ~/actioncam/venv
  
  echo install python packages
  source ~/actioncam/venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
fi
