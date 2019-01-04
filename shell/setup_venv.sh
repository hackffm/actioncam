echo 'set venv'
if [ ! -d ../venv ]; then
	mkdir ../venv
	python3 -m venv ../venv
fi
source '../venv/bin/activate'
