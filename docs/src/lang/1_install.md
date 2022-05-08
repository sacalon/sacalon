# Installation
Requirments :
- python>=3.7
- gcc>=8(or any c++ compiler that supports c++17)
- `libcurl`,`libssl`,`libcrypt`

*Nix :
```bash
git clone https://github.com/hascal/hascal.git
cd hascal
make deps
make build
```

Arch Users :
```bash
pacman -S hascal-git
```

Windows : 
```
git clone https://github.com/hascal/hascal.git
cd hascal
make deps-windows
make windows
```

***Now your Hascal compiler is ready to use in `src/dist` folder, you can add it to `$PATH`.***