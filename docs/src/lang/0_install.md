# Installation
Requirements :
- `python`>=3.7
- `gcc`>=8(or any c++ compiler that supports c++17)
- `libcurl`,`libssl`,`libcrypt`
- `git`(to clone Hascal's source code)

## *Nix Users(recommended)
You can use the `hascal.sh` script to automate the process of installing and adding hascal to `PATH`:
```bash
git clone https://github.com/hascal/hascal.git
cd hascal/
chmod +x ./hascal.sh
bash ./hascal.sh
```

## Windows Users 
```
> git clone https://github.com/hascal/hascal.git
> cd hascal
> make deps-windows
> make windows
```
***Now your Hascal compiler is ready to use in `dist` folder, you can add it to `$PATH`.***

**NOTE**: **The latest version of Hascal should always be used, older versions have bugs when running binary versions of Hascal.**