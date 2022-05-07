# Introduction
[Hascal](https://hascal.github.io) is a general-purpose open source programming language that makes it easy to build simple,optimal, reliable, and efficient software. 

## Installation
Requirments :
- python>=3.7
- gcc>=8(or any c++ compiler that supports c++17)
- `libcurl`,`libssl`,`libcrypt`

*Nix :
```bash
git clone https://github.com/hascal/hascal.git
cd hascal
make deps
make build
```

Arch Users :
```bash
pacman -S hascal-git
```

Windows : 
```
git clone https://github.com/hascal/hascal.git
cd hascal
make deps-windows
make windows
```

***Now your Hascal compiler is ready to use in `src/dist` folder, you can add it to `$PATH`.***

## Hello World
```typescript
function main() : int {
    print("Hello World")
    return 0
}
```
Save this snippet into a file named `hello.has`. Now do: 
```
hascal hello.has
```

Congratulations - you just wrote and executed your first Hascal program!

As in many other languages (such as C++ and Rust), `main` is the entry point of your program and it should return `int` (an integer).

`print` is one of the few built-in functions. It prints the value passed to it to standard output and can be used to print multiple values:
```typescript
function main():int {
    print("Hello World", 42, true)
    return 0
}
```

## Configure the compiler
You can use `config.json` file to configure your Hascal compiler.

The following configuration options are available:
- `compiler` : your c++ compiler name(e.g : `g++`,`clang++`)
- `optimize` : optimize level(0,1,2,3)(default : no optimize)
- `flags` : custom flags(e.g:`["-pthread"]`)
- `no_check_g++` : if you don't use g++, set this to `true`
- `c++_version` : your c++ standard(e.g:`c++17` or `c++20`),**note: c++ version must be greater than or equal to c++17 and compiler must support c++17**
- `g++_out` : if you want to see g++ output, set this to `true`
- `c++_out` : if you want to see generated c++ code, set this to `true`
- `only_compile` if you want to only compile and not link program, set this to `true`

example :

```json
{
    "compiler":"g++",
    "optimize":"-O2",
    "flags":["-pthread"],
    "no_check_g++":1,
    "c++_version":"c++17",
    "g++_out":1,
    "c++_out":1
}
```

## Comments
```typescript
// This is a single line comment
```
NOTE: Multiline comments are not supported yet(TODO).

## Variables
A variable is a named storage for a value. Variables are declared using the `var` keyword :
```typescript
var foo : int = 1
```

Also you can declare a variable without type, in this case, the type will be inferred by the value assigned to it:
```typescript
var foo = 1
```

### Non nullable and nullable
Null safety is a feature that allows you to declare that a variable can be null or not null, and Hascal uses this feature to make sure that your code is safe.

Hascal's variables and constants are non-nullable by default that means that they cannot be null(`NULL`) and you can't assign `NULL` to them and **you should assign a value to them when you declare them**.

```typescript
var foo : int = 1 // non-nullable
var foo_error : int // error : nullable variable must be assigned a value
```

But you can make variables and constants nullable by adding `?` to their type:

```typescript
var bar : int? = 1 // nullable
```

so you can use `NULL` to set a variable to null :

```typescript
bar = NULL // ok
```


## Pointers
Pointers are a way to access the memory address of a variable. You can declare a pointer using the `^` operator after the type:

```typescript
var foo : int^?
```
***NOTE:*** pointers are non-nullable by default, use `?` to make it nullable:

You use cast to assign a value to a pointer:
```typescript
foo = (int^)1
```

Finally, you can use the `^` operator to access the value stored in a pointer:
```typescript
var foo : int^ = (int^)1
print(^foo) // 1
```

NOTE: Currently only one level of pointers are supported.

## Hascal Types

### Primitive types
```typescript
bool // boolean value

string // string literal

int8 uint8 // 8-bit integer
int16 uint16 // 16-bit integer
int int32 uint32 // 32-bit integer
int64 uint64 // 64-bit integer

float // floating point 
double // double floating point
```

### Strings
Strings are a sequence of characters. You can declare a string using the `string` keyword:
```typescript
var foo : string = "Hello World"
```

You can use the `+` operator to concatenate strings:
```typescript
var foo : string = "Hello" + " World"
```

And you can use the `[]` operator to access a character in a string:
```typescript
var foo : string = "Hello"
print(foo[1]) // 'e'
```
> Note: type of accessed character is `char`
> Note: the first character in a string is at index 0.


With `len` function you can get the length of a string:
```typescript
var foo : string = "Hello"
print(len(foo)) // 5
```
> Note: `len` function is a built-in function.

#### Escape sequences
You can use escape sequences to print special characters:
```typescript
var foo : string = "Hello\tWorld"
print(foo) // Hello    World
```

The following escape sequences are supported:
- `\n` : newline
- `\t` : tab
- `\r` : carriage return
- `\\` : backslash
- `\'` : single quote
- `\"` : double quote
- `\?` : question mark
- `\a` : bell
- `\b` : backspace
- `\f` : form feed
- `\v` : vertical tab
- `\0` : null character
- `\x____` : hexadecimal character
- `\u____` : unicode character
- `\U____` : unicode character
- `\_____` : arbitrary octal value 

Note: `_____` means you should specify the id of the character you want to print.

### Numbers
Numbers are either integers or floating point numbers. You can declare a number using the following types:
```typescript
int8 uint8 // 8-bit integer
int16 uint16 // 16-bit integer
int int32 uint32 // 32-bit integer
int64 uint64 // 64-bit integer

float // floating point 
double // double floating point
```

So you can use the following operators to perform arithmetic operations:
- `+` : addition
- `-` : subtraction
- `*` : multiplication
- `/` : division

See the following example:
```typescript
var a : int = 123
var b : float = 1.23
var c : double = 1.2313213215648789798
```

### Type compatibility
Type compatibility is very close to automatic or implicit type conversion. The type compatibility is being able to use two types together without modification and being able to subsititute one for the other without modification.

Compatible types are:
- `int` and `float`
- `int` and `double`
- `float` and `double`

Note: strings are not compatible with characters.

### Arrays
Arrays are collections of data elements of the same type. They can be represented by a list of elements surrounded by brackets. The elements can be accessed by appending an index (starting with 0) in brackets to the array variable:

Arrays declare like following:
```typescript
var foo : [int] = [1,2,3]
var bar : [string] = ["Hello", "World"]
```

You can use the `[]` operator to access an element in an array:
```typescript
var foo : [int] = [1,2,3]
print(foo[1]) // 2
```

And you can assign a value to an array element:
```typescript
var foo : [int] = [1,2,3]
foo[1] = 4
print(foo[1]) // 4
```

With `append` built-in function you can append an element to an array:
```typescript
var foo : [int] = [1,2,3]
foo.append(4)
print(foo[3]) // 4
```

And you can get the length of an array with the `len` built-in function:
```typescript
var foo : [int] = [1,2,3]
print(len(foo)) // 3
```


## If
You can use the `if` keyword to execute a block of code, if a condition is true:
```typescript
var foo : int = 1
if foo == 1 {
    print("foo is 1")
}
```

### Else
You can use the `else` keyword to execute a block of code, if a condition is false:
```typescript
var foo : int = 1
if foo == 1 {
    print("foo is 1")
} else {
    print("foo is not 1")
}
```

### Else if
You can use the `else if` statement to execute a block of code, if `else if` a condition is true:
```typescript
var foo : int = 1
if foo == 1 {
    print("foo is 1")
} else if foo == 2 {
    print("foo is 2")
} else {
    print("foo is not 1 or 2")
}
```

### `and` and `or` and `not`
You can use the `and` keyword to execute a block of code, if all conditions are true:
```typescript
var foo : int = 1
var bar : int = 2
if foo == 1 and bar == 2 {
    print("foo is 1 and bar is 2")
}
```

You can use the `or` keyword to execute a block of code, if at least one condition is true:
```typescript
var foo : int = 1
var bar : int = 2
if foo == 1 or bar == 2 {
    print("foo is 1 or bar is 2")
}
```

You can use the `not` keyword to execute a block of code, if a condition is false:
```typescript
var foo : int = 1
if not foo == 1 {
    print("foo is not 1")
}
```

**You can see Hascal's conditional operators, [here](cond_op/index.html)**

## Loops
You can use the `while` keyword to execute a block of code, if a condition is true:
```typescript
var foo : int = 1
while foo == 1 {
    print("foo is 1")
    foo = 2
}
```

The `for` keyword is used to execute a block of code for a number of times:
```typescript
for i in range(0, 10) {
    print(i)
}
```
Also you can use the `for` keyword for iterating over an array:
```typescript
var foo : [int] = [1,2,3]
for i in foo {
    print(i)
}
```

## Functions
Functions are a way to group code that can be called to perform a specific task. You can declare a function using the `function` keyword:
```typescript
function foo() {
    print("Hello World")
}
```

Also your function block should be outside of a function.

Your function can have parameters and return a value. You can declare parameters and return type, like variable declarations:
```typescript
function add(x:int,y:int): int {
    return x + y
}
```
In the example above, `x` and `y` are parameters and thire type(`int`) is your return type.

> Note: you can use `?` to make a parameter nullable.

### Calling a function
You can call a function by using the function name followed by parentheses:
```typescript
foo()
```
If you want to pass some parameters to your function, you can use them in the parentheses:
```typescript
foo(1,2,3)
```

Also you can assign the return value of a function to a variable:
```typescript
var foo : int = add(1,2)
```

### Function overloading
You can overload functions by changing the number of parameters or the type of parameters :
```typescript
// overloading function
function add(x:int,y:int,z:int): int {
    return x + y + z
}

function add2(x:int,y:int){
    print(x + y)
}

function main(): int {
    print(add(1,2))
    print(add(1,2,3))
}
```

### Passing function as argument
You can pass a function as an argument to another function:
```typescript
function runner(func: Function[int, int]int) : int{
    return func(1,2)
}

function add(a:int, b:int) : int {
    return a+b
}

function main():int {
    print(runner(add))
    return 0
}
```
In the example above, `runner` is a function that takes a function as an argument and returns the return value of the given function.


## Importing modules
You can use other modules by importing them. You can import a module by using the `use` keyword:
```typescript
use os

function main() : int {
   system("start http://www.google.com")
   return 0
}
```

### Importing multiple modules
You can import multiple modules by using the `use` keyword and separating the module names with a comma:
```typescript
use os, math, conv
```

For importing a submodule of a module, you can use the `.` operator:
```typescript
use crypto.sha256
```

### Creating a module
For creating a module, you can create a file with the same name as the module and with the extension `.has` and put the module code inside it:

`add.has`:

```typescript
function add(x:int, y:int) : int {
    return x + y
}
```

`main.has`:
```typescript
use add

function main() : int {
    print(add(1,2))
    return 0
}
```

#### Creating foldered modules
Module files can be placed in a folder, for creating a foldered module you should first create the folder and then create the `_.has` file inside it.
The `_.has` file is the main file of the module and compiler will look for it.
You can also import submodules in `_.has` file.

> Note: Any submodule that is not imported in `_.has` file will be ignored.
> Note: Any submodule can have other submodules.

## Structures
Structures are a way to group data together. You can declare a structure using the `struct` keyword:
```typescript
struct Color {
    var r : int
    var g : int
    var b : int
    var name = "Anything..." // optional
}
```
> Note: Declaring a structure member without a type will make it optional.

After declaring a structure, you can create an instance of it:
```typescript
var red = Color(255,0,0)
```

For accessing the fields of a structure, you should use the `.` operator:
```typescript
var red = Color(255,0,0)
print(red.r)
print(red.g)
print(red.b)
print(red.name)
```

### Structures as return values
You can return a structure from a function:
```typescript
function foo() : Color {
    return Color(1,2,3)
}
```

### Structures as arguments
You can pass a structure as an argument to a function:
```typescript
function foo(c:Color) {
    print(c.r)
    print(c.g)
    print(c.b)
    print(c.name)
}
```

### Structure inheritance
You can inherit a structure from another structure with `:` operator after the structure name:
```typescript
struct RGB : Color {
    
}
```

And you can access the fields of the inherited structure:
```typescript
var foo : RGB = RGB(1,2,3)
print(foo.r,foo.g,foo.b)
   
var bar = RGB(255,0,0,"AColor")
```

## Memory management
Memory management is a way to manage the memory of your program. Hascall use manual memory management because this manual memory management is used in most performance-critical applications like games,OSes, embedded systems, etc.

Hascal uses `new` and `delete` keywords to manage memory, manually.

### Allocation
For allocating memory, you should use the `new` keyword. Note that type of the allocated memory should be pointer or reference type :
```typescript
var foo : int^ = new int(1)
```

For easily declaring and allocating memory, use `var <name> = new <type>(<args...>)` statement, like this:
```typescript
var foo = new int(1)
```

### Reallocation
For reallocating memory and assigning the new value to the pointer, use `<pointer> = new <type>(<args...>)` statement, like this:
```typescript
var foo : int^ = new int(1) // allocate memory
foo = new int(2) // reallocate memory and assign new value
```

### Deallocation
For deallocating memory, you should use the `delete` keyword and pass the pointer to the memory that you want to deallocate:
```typescript
delete foo
```



### Accessing memory
Like pointers, you can access the allocated memory value with the `^` operator:
```typescript
var foo : int^ = new int(1)
print(^foo)
```

### Critical notes
- <span style="color:red">Don't forget to use the `delete` keyword at end of scope and before the end of the program.</span>.
> In future, we will add a feature to show warnings when you forget to use the `delete` keyword.

- **You can't deallocate memory that you haven't allocated it without `new` keyword.**

- **You can allocate, not allocated pointers**:
```typescript
var foo : int^?
foo = new int(1)
```