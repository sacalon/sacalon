# Overview
Sacalon's standard library(`salivan`) is a part of Sacalon programming language. It has been designed to be tiny, simple, useful.

## Design
`salivan` uses C++ codes in backgroud and only we writed some interfaces to C++ files.
Some C++ files written by people outside of Sacalon's community and thier's code licenses are there in [`salivan/libcpp` directory in Sacalon's repository](https://github.com/sacalon-lang/sacalon/tree/main/src/salivan/libcpp). 

list of third-party libraries used in `salivan` :
- [libcurl](https://curl.se/libcurl), [license](https://github.com/sacalon-lang/sacalon/blob/main/src/salivan/libcpp/LICENSE-libcurl).
- [cwalk](https://likle.github.io/cwalk/), [license](https://github.com/sacalon-lang/sacalon/blob/main/src/salivan/libcpp/LICENSE-cwalk).
- [PicoSHA2](https://github.com/okdshin/PicoSHA2), [license](https://github.com/sacalon-lang/sacalon/blob/main/src/salivan/libcpp/LICENSE-picosha2).
- [Argparse](https://github.com/cofyc/argparse), [license](https://github.com/sacalon-lang/sacalon/blob/main/src/salivan/libcpp/LICENSE-argparse).

## Contributing
We welcome contributions of all kinds.

You can contribute to this book by [opening an issue](https://github.com/sacalon-lang/sacalon/issues/new/choose) or [forking](https://github.com/sacalon-lang/sacalon/fork) and [sending a pull request](https://github.com/sacalon-lang/sacalon/compare) to the main Sacalon repository.
Knowing what people use this book for the most helps direct our attention to making those sections the best that they can be. We also want the reference to be as normative as possible, so if you see anything that is wrong, please also file an issue.