# Installation
Requirements :
- `python`>=3.7
- `gcc`>=8(or any c++ compiler that supports c++17)
- `libcurl`,`libssl`,`libcrypt`
- `git`(to clone Sacalon's source code)

## *Nix Users(recommended)
You can use the `sacalon.sh` script to automate the process of installing and adding sacalon to `PATH`:
```bash
git clone https://github.com/sacalon-lang/sacalon.git
cd sacalon/
chmod +x ./sacalon.sh
bash ./sacalon.sh
```

## Windows Users 
```
> git clone https://github.com/sacalon-lang/sacalon.git
> cd sacalon
> make deps-windows
> make windows
```
***Now your Sacalon compiler is ready to use in `dist` folder, you can add it to `$PATH`.***

**NOTE**: **The latest version of Sacalon should always be used. Old versions have bugs when running binary versions of Sacalon.**