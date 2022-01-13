# Makefile for Hascal

build :	
	pyinstaller --noconfirm --onefile --console --name "hascal"  "src/hascal.py"
	cp -r src/hlib dist/	
	cp -r examples/ dist/		
	@echo "\033[0;34m Build succesfully!"
windows :
	pyinstaller --noconfirm --onefile --console --name "hascal"  "src/hascal.py"
	xcopy src\hlib dist\hlib /E /H /C /I
	xcopy examples dist\examples /E /H /C /I
	@echo "\033[0;34m Build succesfully!"

deps :
	python3 --version
	pip3 --version
	pip3 install -r requirements.txt
	@echo "\033[0;36m Installed dependencies!"
deps-windows:
	python --version
	pip --version
	pip install -r requirements.txt
	@echo "\033[0;36m Installed dependencies!"

