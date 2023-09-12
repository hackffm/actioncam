#!/bin/bash
# all files should be in plac by dockerfile
echo "check setup"
if [ ! -d ~/actioncam ]; then
  echo "create actioncam folders"
  mkdir ~/actioncam
  mkdir ~/actioncam/data
  mkdir ~/actioncam/compressed
  mkdir ~/actioncam/log
  mkdir ~/actioncam/recordings
  mkdir ~/actioncam/send
fi
#
if [ ! -f ~/actioncam/config.json ]; then
  echo "copy config"
  cp ./config.json ~/actioncam/
fi
if [ -f ~/actioncam/config.json ]; then
  echo "found config.json and preparing for current user"
  sed -i -e 's/piuser/'"${USERNAME}"'/g' ~/actioncam/config.json
fi
#
if [ ! -f ~/actioncam/config.json ]; then
  echo "copy config"
  cp ./config.json ~/actioncam/
fi
if [ ! -f ~/actioncam/requirements.txt ]; then
  echo "copy requierements.txt"
  cp ./requirements.txt ~/actioncam/
fi
if [ ! -d ~/actioncam/venv ]; then
  mkdir ~/actioncam/venv
  echo "create python venv"
  python3 -m venv ~/actioncam/venv
  
  echo #install python packages"
  source ~/actioncam/venv/bin/activate
  pip install --upgrade pip
  pip install -r ~/actioncam/requirements.txt
fi
if [ ! -f ~/actioncam/code ]; then
  echo "copy code"
  cp -r ../../code ~/actioncam/
fi
if [ ! -f ~/actioncam/start_actioncam.sh ]; then
  echo "copy start_actioncam.sh"
  cp ../startup/start_actioncam.sh ~/actioncam/
fi
