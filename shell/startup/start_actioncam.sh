#!/usr/bin/env bash
echo 'set absolute path to venv'
actioncam_dir='/home/pi/git/actioncam/'
source $actioncam_dir'venv/bin/activate'
python $actioncam_dir'code/actioncam.py'

