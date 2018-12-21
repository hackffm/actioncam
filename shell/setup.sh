#!/bin/bash
sudo apt update && sudo apt dist-upgrade
sudo apt install python3-venv opencv*
python3 -m pip install --upgrade pip
if [ ! -d ../venv ]; then
	mkdir ../venv
	python3 -m venv ../venv
fi
