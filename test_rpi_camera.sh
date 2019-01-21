#!/bin/bash

if [ ! -d ~/temp/camera ]; then
    mkdir -p ~/temp/camera
fi

DATE=$(date +"%Y-%m-%d_%H%M")
raspistill -vf -hf -o ~/temp/camera/$DATE.jpg
echo "created ~/temp/camera/$DATE.jpeg"
