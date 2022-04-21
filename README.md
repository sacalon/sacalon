
<div align="center">
  <img style="text-align:center" src="hascal-logo.png" height="128px" width="128px">


  # The Hascal Programming Language

  [Website](https://hascal.github.io) |
  [Docs](https://hascal.github.io/docs/latest) |
  [Changelog](docs/CHANGELOG.md) |
  [Roadmap](docs/ROADMAP.md)

  [IDE Integration](docs/ide.md) |
  [Library Index](https://github.com/hascal/libs) |
  [AUR Package](https://aur.archlinux.org/packages/hascal-git)

  [![](https://img.shields.io/gitter/room/hascal/community?style=for-the-badge)](https://gitter.im/hascal/community)
 
</div>

**Hascal** is a general purpose and open source programming language designed to build optimal, maintainable, reliable and efficient software.
> **NOTES:** 
> - Hascal is still in the very early stages of development.
> - Hascal pronounces like "Pascal".

## Features
- [x] Easy to use and easy to learn
- [x] Fast and powerful like C++
- [x] Inspired by Swift, Pascal and a bit Haskell
- [x] Functional programming
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
        plus(
            x,
            y
        ),
        z
    )

    var avg = divide(
        sum,
        3
    )

    print("Sum :",sum)
    print("Average :",avg)

    return 0
}
```

> You can see more Hascal examples in [examples folder](https://github.com/hascal/hascal/tree/main/examples).

## Documentation
> You can find Hascal's documentation, [Here](https://hascal.github.io/docs)

## Contributions
Any contribution is welcome :)

[See our roadmap](docs/roadmap.md)

<!-- [![graph](https://contrib.rocks/image?repo=hascal/hascal)](https://github.com/hascal/hascal/graphs/contributors)
-->
## License
The compiler and standard libraries are licensed under the **"MIT License"**,
Read the [License](https://github.com/hascal/hascal/blob/main/LICENSE) for more information.

## About
Copyright © 2019-2022 **Hascal Foundation**, \
all rights reserved.

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
