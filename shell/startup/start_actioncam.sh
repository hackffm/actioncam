#!/usr/bin/env bash
actioncam_dir='~/actioncam'
source "${actioncam_dir}/venv/bin/activate"
cd "${actioncam_dir}/code"
python actioncam.py
