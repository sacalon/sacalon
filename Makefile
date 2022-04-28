 # Makefile for Hascal

build :
	pyinstaller --noconfirm --onefile --console --name "hascal"  "src/hascal.py"
	cp -r src/hlib dist/	
	cp -r examples/ dist/	
windows :
	pyinstaller --noconfirm --onefile --console --name "hascal"  "src/hascal.py"
	xcopy src\hlib dist\hlib /E /H /C /I
	xcopy examples dist\examples /E /H /C /I
deps :
	python3 --version
	pip3 --version
	pip3 install -r requirements.txt
deps-windows:
	python --version
	pip --version
	pip install -r requirements.txt
path:
	cp src/dist/hascal usr/local/bin/hascal
