@ECHO OFF
cd src
cls
python --version
echo =====================
pip --version
echo =====================
echo Installing Packages...
pip install -r requirements.txt
echo =====================
echo Building...
pyinstaller --noconfirm --onefile --console --name "hascal"  "src/hascal.py"
