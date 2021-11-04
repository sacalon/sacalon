# Makefile for Hascal

build :
	pyinstaller --noconfirm --onefile --console --name "hascal"  "src/hascal.py"
	cp -r src/hlib dist/	
	cp -r examples/ dist/	

windows :
    pyinstaller --noconfirm --onefile --console --name "hascal"  "src/hascal.py"
	xcopy src\hlib dist\hlib /E /H /C /I
	xcopy examples dist\examples /E /H /C /I
	
buildtest:
	cp -r src/hlib dist/	
	cp -r examples/ dist/	
	
wintest :
	xcopy src\hlib dist\hlib /E /H /C /I
	xcopy examples dist\examples /E /H /C /I
deps :
	python --version
	pip --version
	pip install -r requirements.txt
