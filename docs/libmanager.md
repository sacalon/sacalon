# Hascal Library Manager(HLM)

**HLM** is default and builtin Hascal's library manager.

## Install a library
```
$ hascal install <library name>
```

example :
```
$ hascal install log
```

## Uninstall a library
```
$ hascal uninstall <library name>
```

example :
```
$ hascal uninstall log
```

## Publish you libraries
You can publish your library and users can install it with hlm.
Steps :
- Fork [this repo](https://github.com/hascal/libs)
- Clone your forked repo
- Add a directory contains your library name
```
$ mkdir <your library name>
```
- Put your library source in created directory
- Open `index.json` file and add your library with following template(don't change anything only add your information) :
`index.json` :
```json
{
    ...
    "your library name" : {
        "author" : "", // your name
        "files" : ["file1.has","file2.has",...] // your files name should be included
    }
    ...
}
```