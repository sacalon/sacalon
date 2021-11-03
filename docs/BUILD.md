# Build from source

Prequistes :

- python v3.8 or higher
- pyinstaller 
- a build of [dmd](https://dlang.org/) compiler

<hr>
- At first clone hascal repo :
```
$ git clone https://github.com/hascal/hascal
$ cd hascal
```
- Install prequistes(if you already installed prequistes, skip this part) :
```
$ make deps
```

- Build with pyinstaller :
```
$ make
```

Now put `src/hlib` folder in `src/dist`, and excutable files exists in `src/dist` folder.


## Set `HASCAL_ROOT`
Hascal for find its standrad libraries, must use `HASCAL_ROOT` environment variable. You should set hascal's compiler folder to `HASCAL_ROOT` environment variable:
```
$ set HASCAL_ROOT = /path/to/your/hascal/compiler/
```
