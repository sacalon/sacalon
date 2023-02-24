<div align="center">
  <img style="text-align:center" src="hascal-logo.png" height="128px" width="128px">

  # The Hascal Programming Language

  [Website](https://hascal.github.io) |
  [Docs](https://hascal.github.io/docs/latest) |
  [Coding Style](https://hascal.github.io/style.html) |
  [Changelog](docs/src/CHANGELOG.md) |
  [Roadmap](docs/src/ROADMAP.md)
  
  <!-- [AUR Package](https://aur.archlinux.org/packages/hascal-git)
  [![](https://img.shields.io/aur/version/hascal-git?label=AUR%20Package&logo=linux)](https://aur.archlinux.org/packages/hascal-git)
  -->
  [![](https://img.shields.io/github/v/tag/hascal/hascal)](https://github.com/hascal/hascal/releases)
  [![Hascal Discord](https://img.shields.io/discord/932745959190978683?color=blue&label=Discord&logo=discord&logoColor=green)](https://discord.gg/rg4T2zBmyv)
  [![](https://img.shields.io/gitter/room/hascal/hascal?logo=gitter)](https://gitter.im/hascal/community)
  

</div>

**Hascal** is a general purpose and open source programming language designed to build optimal, maintainable, reliable, and efficient software.

> **NOTES:**
> - Hascal is still in the very early stages of development.
> - Hascal pronounces like "Pascal".

## Features

- [x] Easy to use and easy to learn
- [x] Multi-paradigm
- [x] Null safety by default
- [x] Fast and powerful
- [x] Inspired by Swift and Pascal(Hascal is based on the good ideas of the Pascal language)
- [x] Manual memory management
- [x] Compiles to C++
- [x] Compatible with C\C++\Obj-C
- [x] [Builtin compile-time FFI system](https://hascal.github.io/docs/latest/lang/14_interfacing_with_cpp.html)
- [x] Built-in HTTP Library

## Examples

Hello World :

```typescript
function main() : int {
    print("Hello World!")
    return 0
}
```

HTTP Request:

```typescript
use http
function main() : int {
    var content = get("https://www.google.com")
    print(content)
    return 0
}
```

Regex match:

```typescript
use regex

function main() : int {
    var matched : bool = regex("subject","(sub)(.*)")
    print(matched) // Output : 1
    return 0
}
```

> You can see more Hascal examples in [examples directory](https://github.com/hascal/hascal/tree/main/examples).

## Documentation

> You can find Hascal's documentation, [Here](https://hascal.github.io/docs/latest).

## Contributions

You can contribute to Hascal by [opening an issue](https://github.com/hascal/hascal/issues/new/choose) and [forking](https://github.com/hascal/hascal/fork) the repository or [contributing to Hascal's documentation](https://github.com/hascal/hascal/tree/main/docs).

You can also join the Hascal community on [Gitter](https://gitter.im/hascal/community) or [Discord](https://discord.gg/rg4T2zBmyv) and ask & answer questions.

[See our roadmap](docs/src/ROADMAP.md)

<!-- [![graph](https://contrib.rocks/image?repo=hascal/hascal)](https://github.com/hascal/hascal/graphs/contributors) -->

## License

The compiler and standard libraries licensed under the **"3-Clause BSD License"**,
read the [License](https://github.com/hascal/hascal/blob/main/LICENSE) for more information.

## About

Copyright © 2019-2023 **Hascal Foundation**, \
all rights reserved.

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
