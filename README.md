
<div align="center">
  <img style="text-align:center" src="hascal-logo.png" height="128px" width="128px">


  # The Hascal Programming Language
  [![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/hascal/community)
  [![linked in](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/company/hascal-lang)
</div>


**Hascal** is a **simple**, **fast**, **powerful** and **compiled systems** programming language. It's designed to be an alternative to C\C++ with a easy syntax.

<!-- > Visit [Hascal's Official Website](https://hascal.github.io) -->
> **NOTE:** Hascal is currently under development.
## Features
- [x] Cross Platform (Linux, Windows, MacOS, BSD، Android & iOS, Embedded Systems) 
- [x] Fast & Powerful
- [x] Easy to learn
- [x] C-Family syntax, inspired by Swift, TypeScript
- [x] Compiles to binary with [dmd](https://github.com/dlang/dmd)
- [x] Native binaries with no dependency
- [x] Garbage Collection and Manual Memory Allocation

## Examples
Hello World :
```typescript
function main() : int {
    print("Hello World!")
    return 0
}
```
Read from stdin :
```typescript
function main() : int{
    print("Enter your name :")
    var name = ReadStr()
    print("Hi,",name)
    return 0
}
```
> You can see more Hascal examples in [examples folder](https://github.com/hascal/hascal/tree/main/examples).

## Documentation
> You can find documentations on installation and using Hascal, [Here](https://github.com/hascal/hascal/tree/main/docs)

## Build from source
> See [build help page](BUILD.md)

## License
The compiler and the standard libraries are licensed under the **"GNU general public license v3"**,
Read the [License](https://github.com/hascal/hascal/blob/main/LICENSE) for more details.

## About
Copyright ©2019-2022 **Hascal Foundation**, \
all rights reserved.

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
