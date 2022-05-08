# Interfacing with C++
Hascal is based on C++, so you can use C++ functions and classes in your program.

## Inline C++ Code
You can use inline c++ code in Hascal with `cuse` keyword :
```typescript
cuse '#include <cstdio>'
cuse 'int main(){printf("%d",1);return 0;}'
// output : 1
```

Or you can use multiline c++ code, like following:
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

## Include C++ headers
Also Hascal can include C++ headers in your program.
We need two files, one for including macros and one for main part of the header. You should put including macros in `your_cpp_lib.hpp` and main part in `your_cpp_lib.cc`. The specified files should exist in the same folder.

See the example below:

`add.cc` :
```cpp
void cpp_print(int x){
    printf("%d",x);
}
```

`add.hpp` :
```cpp
#include <cstdio>
```

`main.has` :
```typescript
cuse add 

function cpp_print(x:int)

function main() : int {
    cpp_print(12)
    return 0
}
```
