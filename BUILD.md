# Build from source

Prequistes :

- python v3.8 or higher
- pyinstaller 
- a build of [dmd](https://dlang.org/) compiler

<hr>

## Install Pyinstaller

>Enter the following command in your terminal
```
pip install pyinstaller
```

if use Linux :
```
pip3 install pyinstaller
```

## DMD Compiler
Hascal for generate binary code use dmd you should put a version of dmd compiler in the folder of Hascal compiler.

## Build
For build Hascal enter following command in terminal :
```sh
pyinstaller hascal.py --onefile
```
or
```sh
pyinstaller --noconfirm --onefile --console --name "hascal"  "hascal.py"
```


Excutable file compiled in src/dist folder.

## Set `HASCAL_ROOT`
Now set `HASCAL_ROOT` environment variable to hascal root folder.

If you want information about setting it up on your maching, visit this bog on dev.to - https://dev.to/pranavbaburaj/introducing-hascal-part-1-5h1f
