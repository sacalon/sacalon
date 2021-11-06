# Hascal's Roadmap for v1.3.

## Base
- C++ in back-end
- garbage collection and rust-like memory management

## Language
- multi library import :
```
use http, random
```

- inline assembly
```
asm("mov e1, bx")
```

- multi line string
``` 
var str = """line1
line2
"""
```

- function decorators :
```
@no_gc
@static
function add(a:int,b:int) : int {
    return a + b
}
```
- lambdas :
```
var mythread = thread(@(1000,true){
    print("hi")
})
```

- dictionaries :
```
var names_age = dict(string,{
   "john" : 25,
   "nickolas" : 38
})

# or :
var foo : dict = (string,{
   "X" : 1,
   "Y" : 2
})
```

- optional function's argument
```
function foo(x:int,y:int,z:int=1){
    print(x*y*z)
}
foo(1,2)
```

- immutable variables
```
var imut x : int = 1
```

- builtin string formation method
```
var x = 1
var y = 2
print(format("x is {}, y is {},x,y))
```

## Standard Library
- `json` library
