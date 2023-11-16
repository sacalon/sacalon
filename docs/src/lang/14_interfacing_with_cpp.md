# Interfacing with C++
Sacalon is based on C++, so you can use C++ functions and classes in your program.

## Inline C++ Code
You can use inline c++ code in Sacalon with `cuse` keyword :
```typescript
cuse '#include <cstdio>'
cuse 'int main(){printf("%d",1);return 0;}'
// output : 1
```

Or you can use multiline c++ code, like following example:
```typescript
cuse """
#include <cstdio>

int main(){
    printf("%d",1);
    return 0;
}
"""
```

## Externing functions
For using C++ functions in your program, you should at first declare them with following syntax:
```typescript
function <name>(<args...>) : <return type>
```
Example :
```typescript
function system(command:char^):int
```

## Include C++ headers
Also Sacalon can include C++ headers in your program.
We need two files, one for headers and one for main part of the library. You should put `#include`,... in `your_cpp_lib.hpp` and main part of library in `your_cpp_lib.cc`. The specified files should exist in the same folder.

See the example below:

`add.cc` :
```cpp
void __sacalon__cpp_print(int x){
    printf("%d",x);
}
```
> add `__sacalon__` to your C++ functions, structs name. Sacalon transpiles to C++ and it adds `__sacalon__` prefix to your C++ names.

`add.hpp` :
```cpp
#include <cstdio>
```

`main.sa` :
```typescript
cuse add 

function cpp_print(x:int)

function main() : int {
    cpp_print(12)
    return 0
}
```

Also you can put the C++ files in a folder and rename they to `_.cc` and `_.hpp`.

**Note that don't include local headers in `*.hpp` file.**

## Accessing to values and types in inline C++ code
You can access to Sacalon's variable and types in inline C++ codes in Sacalon by adding `__sacalon__` prefix to a name, for example:
`main.sa`:
```typescript
function add(a:int,b:int){
    cuse """
        std::cout << a + b;
    """
}
```

you can return a value in inline C++ codes by returning a meaningless value with same type as return type of the function(it may be ridiculous, we are currently working to improve it):
```typescript
function add(a:int,b:int){
    cuse """
        return a + b;
    """
    return 0 // return a value with same type as return type of the function
}
```