# Makefile for Hascal

build :
	pyinstaller --noconfirm --onefile --console --name "hascal"  "src/hascal.py"
	copy -r src/hlib dist/	

windows :
	pyinstaller --noconfirm --onefile --console --name "hascal"  "src/hascal.py"
	xcopy src\hlib dist\hlib /E /H /C /I

deps :
	python --version
	pip --version
	pip install -r requirements.txt