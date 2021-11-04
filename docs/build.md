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
***Now your Hascal compiler is ready to use!!!***
