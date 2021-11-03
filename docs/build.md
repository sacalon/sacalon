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

- Build hascal excutable file :

  - On POSIX(linux,macOS,BSDs) :
  ```
  $ make
  ```
  - On Windows :
  ```
  $ make windows
  ```

## Set `HASCAL_ROOT`
Hascal for find its standrad libraries, must use `HASCAL_ROOT` environment variable. You should set hascal's compiler folder to `HASCAL_ROOT` environment variable.

POSIX :
```
$ export HASCAL_ROOT = /path/to/your/hascal/compiler/
```

Windows :
```
$ set HASCAL_ROOT = /path/to/your/hascal/compiler/
```
or you can set `HASCAL_ROOT` in windows with windows control panel.

***Now your Hascal compiler is ready to use!!!***
