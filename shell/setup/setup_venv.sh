echo create additional venv folder
if [ ! -d ~/actioncam/venv ]; then
	mkdir ~/actioncam/venv
	python3 -m venv ~/actioncam/venv
fi
