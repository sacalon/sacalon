<div align="center">
  <img style="text-align:center;border-radius:50%;" src="logo.jpeg" height="128px" width="128px">

  # The Sacalon Programming Language

  [Website](https://sacalon.github.io) |
  [Docs](https://sacalon.github.io/docs/latest) |
  [Coding Style](https://sacalon.github.io/style.html) |
  [Changelog](docs/src/CHANGELOG.md) |
  [Roadmap](docs/src/ROADMAP.md)
  
  [![](https://img.shields.io/github/v/tag/sacalon-lang/sacalon)](https://github.com/sacalon-lang/sacalon/releases)
  [![Sacalon Discord](https://img.shields.io/discord/932745959190978683?color=blue&label=Discord&logo=discord&logoColor=green)](https://discord.gg/rg4T2zBmyv)
  [![](https://img.shields.io/gitter/room/sacalon-lang/sacalon?logo=gitter)](https://gitter.im/sacalon/community)
  

</div>

[![ReadMeSupportPalestine](https://raw.githubusercontent.com/Safouene1/support-palestine-banner/master/banner-project.svg)](https://github.com/Safouene1/support-palestine-banner)

**Sacalon** is a general purpose and open source programming language designed to build optimal, maintainable, reliable, and efficient software.

> [!IMPORTANT]  
> - Sacalon is still in the very early stages of development.

## Features

- [x] Easy to use and easy to learn
- [x] Multi-paradigm
- [x] Null safety by default
- [x] Fast and powerful
- [x] Inspired by Swift and Pascal(Sacalon is based on the most effective ideas of the Pascal language)
- [x] Manual memory management
- [x] Compiles to C++
- [x] Compatible with C\C++\Obj-C
- [x] [Builtin compile-time FFI system](https://sacalon.github.io/docs/latest/lang/14_interfacing_with_cpp.html)
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

> You can see more Sacalon examples in [examples directory](https://github.com/sacalon-lang/sacalon/tree/main/examples).

## Documentation

> You can find Sacalon's documentation, [Here](https://sacalon.github.io/docs/latest).

## Contributions

You can contribute to Sacalon by [opening an issue](https://github.com/sacalon-lang/sacalon/issues/new/choose) and [forking](https://github.com/sacalon-lang/sacalon/fork) the repository or [contributing to Sacalon's documentation](https://github.com/sacalon-lang/sacalon/tree/main/docs).

You can also join the Sacalon community on [Gitter](https://gitter.im/sacalon/community) or [Discord](https://discord.gg/rg4T2zBmyv) and ask & answer questions.

![Alt](https://repobeats.axiom.co/api/embed/f35044c25fa7a09ff17ef5abd0ffda29de68e142.svg "Repobeats analytics image")

<a href="https://github.com/sacalon-lang/sacalon/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=sacalon-lang/sacalon" />
</a>

<!-- [![graph](https://contrib.rocks/image?repo=sacalon-lang/sacalon)](https://github.com/sacalon-lang/sacalon/graphs/contributors) -->

## License
The compiler and standard libraries are licensed under the **"3-Clause BSD License"**. Read the [License](https://github.com/sacalon-lang/sacalon/blob/main/LICENSE) for more information.

## About

Copyright © 2019-2024 **Sacalon Foundation**, \
all rights reserved.

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
