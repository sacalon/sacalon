$python=python
$pip=pip3
$pyinstaller=pyinstaller

$pip install -r requirements.txt
$python -m $pyinstaller --noconfirm --onefile --console --name "hascal"  "src/hascal.py"
cp -r src/hlib dist/	
cp -r examples/ dist/