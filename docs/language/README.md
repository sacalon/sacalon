# Hascal Documentation

[Hascal](https://hascal.github.io) is a general-purpose open source programming language that makes it easy to build simple,optimal, reliable, and efficient software. 

## Installation
Prequistes :
- python v3.8 or higher
- pyinstaller 
- GCC/G++ on your `$PATH`

First clone Hascal's source :
```
$ git clone https://github.com/hascal/hascal
```

Install prequistes(not gcc only python libs,if you already installed prequistes, skip this part):
```
$ make deps
```

Build hascal excutable file :
  - On POSIX(Linux,MacOS,BSDs) :
  ```
  $ make
  ```
  - On Windows :
  ```
  $ make windows
  ```

***Now your Hascal compiler is ready to use in `src/dist` folder!!!***
NOTE: But you can add Hascal to `$PATH` for easily use.

## Hello World
```c#
function main() : int {
    print("Hello World")
    return 0
}
```
Save this snippet into a file named `hello.has`. Now do: `hascal hello.has`.

Congratulations - you just wrote and executed your first Hascal program!

As in many other languages (such as C++ and Rust), `main` is the entry point of your program.

`print` is one of the few built-in functions. It prints the value passed to it to standard output.

## Comments
```py
# This is a single line command
```

## Variables
```c#
var foo : int
var foobar : int = 1

var bar = 1
function main() : int {
    print(foo,foobar)
    return 0
}
```

## Functions
```c#

```

## Hascal Types

### Primitive types
```nim
bool # boolean value

string # string literal

int # integer value

float # floating point 
double # double floating point(soon)
```

### Strings
```c#
function main() : int {
    var text = "Hello World"
    print(text[0]) # output : H 

    var text2 = "Hello\tWorld"
    print(text2) # output : Hello   World
    return 0
}
```

### String operators
```c#
function main() : int {
    var text = "Hello "
    print(text + "World") # output : Hello World 
    return 0
}
```
All operators in Hascal must have values of the same type on both sides. You cannot concatenate an integer to a string:
```c#
function main() : int {
    var text = "age = "
    var age = 23
    print(text + age) # error : Mismatched type 'string' and 'int' :2 
    return 0
}
```
We have to either convert age to a string:
```c#
function main() : int {
    var text = "age = "
    var age = 23
    print(text + to_string(age)) # error : Mismatched type 'string' and 'int' :2 
    return 0
}
```