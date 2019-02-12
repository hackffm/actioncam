#!/bin/bash
echo "create actioncam folders"
if [ ! -d ~/actioncam ]; then
	mkdir ~/actioncam
	mkdir ~/actioncam/log
	mkdir ~/actioncam/recording

    cp config.json ~/actioncam
fi
