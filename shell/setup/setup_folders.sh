#!/bin/bash
echo create actioncam folder
if [ ! -d ~/actioncam ]; then
	mkdir ~/actioncam
	mkdir ~/actioncam/log
	mkdir ~/actioncam/recording
fi
