# Overview
Hascal's standard library(`hlib`) is a part of Hascal programming language. It has been designed to be tiny, simple, useful.

## Design
`hlib` uses C++ codes in backgroud and only we writed some interfaces to C++ files.
Some C++ files written by people outside of Hascal's community and thier's code licenses are there in [`hlib/libcpp` directory in Hascal's repository](https://github.com/hascal/hascal/tree/main/src/hlib/libcpp). 

list of third-party libraries used in `hlib` :
- [libcurl](https://curl.se/libcurl), [license](https://github.com/hascal/hascal/blob/main/src/hlib/libcpp/LICENSE-libcurl).
- [cwalk](https://likle.github.io/cwalk/), [license](https://github.com/hascal/hascal/blob/main/src/hlib/libcpp/LICENSE-cwalk).
- [PicoSHA2](https://github.com/okdshin/PicoSHA2), [license](https://github.com/hascal/hascal/blob/main/src/hlib/libcpp/LICENSE-picosha2).
- [Argparse](https://github.com/cofyc/argparse), [license](https://github.com/hascal/hascal/blob/main/src/hlib/libcpp/LICENSE-argparse).

## Contributing
We welcome contributions of all kinds.

You can contribute to this book by [opening an issue](https://github.com/hascal/hascal/issues/new/choose) or [forking](https://github.com/hascal/hascal/fork) and [sending a pull request](https://github.com/hascal/hascal/compare) to the main Hascal repository.
Knowing what people use this book for the most helps direct our attention to making those sections the best that they can be. We also want the reference to be as normative as possible, so if you see anything that is wrong, please also file an issue.