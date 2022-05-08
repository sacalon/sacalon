# Hascal's Changelog
<details>
<summary>v1.3.9</summary>

<details>
<summary>v1.3.9-beta</summary>

#### New features
- passing functions as arguments
```typescript
function f(x: int): int {
    return x + 1
}

function g(func:Function[int]int): int {
    return func(1)
}
```
- add static variables, [See this example](https://github.com/hascal/hascal/blob/main/tests/static.has)
- add `only_compile` config option

#### Changes
- upgrade importing system

#### Bug fixes

#### Removed

</details>

<details>
<summary>v1.3.9-alpha.1</summary>

#### Changes
- add `download`,`upload`,`post` functions to `http` library
- `https` support for `http` library
- add `windows` library(that includes `windows.h`)
- add `browser` library to open urls in default browser(now only supports windows)

#### Bug fixes
- fix linker flag import bug in `cuse` statement

</details>

</details>


<details>
<summary>v1.3.8</summary>

#### New features
- non-nullable and nullable variables

#### Changes
- change pointer unary from `*` to `^`
- improve importing system

#### Bug fixes
- fix repetitious imports bug
- fix #29 bug(by [@mmdbalkhi](https://github.com/mmdbalkhi))
  
#### Removed
- remove `token` library

</details>

<details>
<summary>v1.3.7</summary>

#### New features
- manual memory management with `new` and `delete` keyword
- functional programming paradigm
- speed up compilation time
- add `typeof` function
- now can print arrays and structures
- function decorators
- `static` and `extern` decorator
- multiple library import
- improve importing system
- improve stdlib architecture

#### Bug fixes
- fix scoping bug
- fix `conv` library bug
- fix conditions bug

#### Removed
- `export` library removed
- `local use` statement removed

</details>

<details>
<summary>v1.3.6</summary>
  
#### New features
- more data types : `int8`,`uint8`,`int16`,`uint16`,`int32`,`uint32`,`int64`,`uint64`,`double`
- type compatibility
- multi line string
- pointers and references
```typescript
var x : *int = 20
var y : int = 10
x = &y
var z = *x // type : int

// Pointers fix incomplete types on struct defination
struct bar {
    var self : *bar
}
```
- add `sizeof` function

#### Bug fixes
- fix lexer bugs
- check if function returns a value at end of string else show error
- `main` function should returns int
- fix `termcolor` library bugs
- fix enum bugs

#### Standart library
- add `sdl2` wrapper
- add `export` library for exporting to C(see : [haspy](https://github.com/bistcuite/haspy))
- add `crypto.sha256` for sha256 hashing

#### Removed
- `libcinfo` library removed

</details>


<details>
<summary>v1.3.5</summary>

#### Standard library
##### Updated
`os` :
- add `compiler_name` function to get the name of the compiler
- add `arch` function to get the architecture of the system
- add `is_x86` function to check if the architecture is x86
- add `is_x64` function to check if the architecture is x64
- add `getenv` function to get an environment variable
##### Added
- add `libcinfo` library to get information about the libc
- add `termcolor` library to colorize the output

![assets/termcolor.png](assets/termcolor.png)

#### Bug fixes
- Fix incomplete type defination bug

</details>

<details>
<summary>v1.3.4</summary>
  
#### New features
- compiler option : now can generate c++ code from hascal code with `c++_code : 1` in `config.json` file
- use `cuse` keyword to include c++ files.

#### Bug fixes
- Fix semantic analyser bugs
- Fix standard library bug

</details>

<details>
<summary>v1.3.3</summary>

#### New features
- struct inheritance
- can use `cuse` statement on struct declaration

#### Bug fixes
- Fix variable scope bug
- Fix variable declaration bug
- Fix semantic analyser bug

</details>

<details>
<summary>v1.3.2</summary>

#### New features
- `for in` statement
- library manager
- flag option
- `cuse` statement

#### Bug fixes
- Fix semantic analyser bugs
- Fix nested struct bug

#### Removed
- `for to` and `for downto` statement removed

</details>

<details>
<summary>v1.3.1</summary>

#### New features
- Basic Semantic Anaslyser

#### Removed
- remove semicolon from syntax

</details>