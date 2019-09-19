#!/bin/bash
if [ ! -d ~/actioncam ]; then
  echo "create actioncam folders"
	mkdir ~/actioncam
	mkdir ~/actioncam/data
	mkdir ~/actioncam/log
	mkdir ~/actioncam/recording
	echo "prepare config"
  cp config.json ~/actioncam
  sed -i -e 's/pi/'"${USER}"'/g' ~/actioncam/config.json
fi
