$python=python3
$pip=pip3
$pyinstaller=pyinstaller

cd src
clear
$python --version
echo "====================="
$pip --version
echo "====================="
echo "Installing Packages..."
$pip install -r requirements.txt
echo "====================="
echo "Building..."
$pyinstaller --noconfirm --onefile --console --name "hascal"  "hascal.py"
