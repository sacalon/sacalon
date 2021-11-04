

pip3 install -r ./requirements.txt
python -m pyinstaller --noconfirm --onefile --console --name "hascal"  "src/hascal.py"
cp -r ./src/hlib ./dist/	
cp -r ./examples/ ./dist/