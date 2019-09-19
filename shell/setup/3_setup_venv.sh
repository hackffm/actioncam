echo create additional venv folder
sudo pip3 install --upgrade pip
if [ ! -d ~/actioncam/venv ]; then
	mkdir ~/actioncam/venv
	python3 -m venv ~/actioncam/venv
fi
