
<div align="center">
  <img style="text-align:center" src="hascal-logo.png" height="128px" width="128px">


  # The Hascal Programming Language

  [Website](https://hascal.github.io) |
  [Docs](https://hascal.github.io/docs/latest) |
  [Changelog](docs/src/CHANGELOG.md) |
  [Roadmap](docs/src/ROADMAP.md) |
  [IDE Integration](docs/src/ide.md)
  
  <!-- [AUR Package](https://aur.archlinux.org/packages/hascal-git) -->
  [![](https://img.shields.io/github/v/tag/hascal/hascal)](https://github.com/hascal/hascal/releases)
  [![Hascal Discord](https://img.shields.io/discord/932745959190978683?color=blue&label=Discord&logo=discord&logoColor=green)](https://discord.gg/yjv8QqPR)
  [![](https://img.shields.io/gitter/room/hascal/hascal?logo=gitter)](https://gitter.im/hascal/community)
  [![](https://img.shields.io/aur/version/hascal-git?label=AUR%20Package&logo=linux)](https://aur.archlinux.org/packages/hascal-git)


</div>

**Hascal** is a general purpose and open source programming language designed to build optimal, maintainable, reliable and efficient software.
> **NOTES:** 
> - Hascal is still in the very early stages of development.
> - Hascal pronounces like "Pascal".

## Features
- [x] Easy to use and easy to learn
- [x] Multi-paradigm
- [x] Null safety by default
- [x] Fast and powerful
- [x] Inspired by Swift, Pascal and a bit Haskell
- [x] C++ on backend
- [x] Compatible with C\C++\Obj-C

## Examples
Hello World :
```typescript
function main() : int {
    print("Hello World!")
    return 0
}
```

Formatting Strings :
```typescript
function main() : int {
    var name = ReadStr("Enter your name :")
    var fmt_str = format("Hi,{}",name)
    print(fmt_str)
    return 0
}
```

Functional Programming :
```typescript
use functional

function main() : int {
    var x = 1
    var y = 2
    var z = 3

    var sum = plus(
        plus(x,y),z
    )

    var avg = divide(sum,3)

    print("Sum :",sum)
    print("Average :",avg)

    return 0
}
```

> You can see more Hascal examples in [examples folder](https://github.com/hascal/hascal/tree/main/examples).

## Documentation
> You can find Hascal's documentation, [Here](https://hascal.github.io/docs/latest)

## Contributions
You can contribute to Hascal by [opening an issue](https://github.com/hascal/hascal/issues/new/choose) or [forking](https://github.com/hascal/hascal/fork) the repository and [contributing to Hascal's documentation](https://github.com/hascal/hascal/tree/main/docs).

You can also [join the Hascal community](https://gitter.im/hascal/community) and ask questions.

[See our roadmap](docs/src/ROADMAP.md)

<!-- [![graph](https://contrib.rocks/image?repo=hascal/hascal)](https://github.com/hascal/hascal/graphs/contributors) -->


## License
The compiler and standard libraries are licensed under the **"MIT License"**,
Read the [License](https://github.com/hascal/hascal/blob/main/LICENSE) for more information.

## About
Copyright © 2019-2022 **Hascal Foundation**, \
all rights reserved.

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
