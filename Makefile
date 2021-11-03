# Makefile for Hascal

build :
	pyinstaller --noconfirm --onefile --console --name "hascal"  "src/hascal.py"	

deps :
	python --version
	pip --version
	pip install -r requirements.txt