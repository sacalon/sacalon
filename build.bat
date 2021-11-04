pip install -r requirements.txt
pyinstaller --noconfirm --onefile --console --name "hascal"  "src/hascal.py"
xcopy src\hlib dist\hlib /E /H /C /I
xcopy examples dist\examples /E /H /C /I