# Hascal's Roadmap 

<details>
<summary>v1.3.x</summary>

### Base
- C++ in back-end
- `new/delete` c++ keyword based memory management
- null safety
- basic support for pointers
- use `std::array` for fixed sized array instead of `std::vector`
- check if a function returns a value, else show error
- redesign logo

### Language
- multi library import :
```
use http, random
```

- inline assembly
```
asm("mov e1, bx")
```

- lambdas :
```
var mythread = thread(@(1000,true){
    print("hi")
})
```

- function decorators :
```
@static
function add(a:int,b:int) : int {
    return a + b
}
```

- `@no_mm` decorator for manual memory management
- `@extern_c` decorator defines a function or variable in an `extern "C"` block 

- dictionaries :
```
var names_age = dict(string,int,{
   "john" : 25,
   "nickolas" : 38
})

# or :
var foo = {
   "X" : 1,
   "Y" : 2
}
```

- namespace based library import
e.g:
`foo.has` :
```
function bar(): string {
    return "bar"
}
```

`main.has` :
```
use foo

function main () : int {
    print(foo::bar())
    return 0
}
```
### Standard Library
- `json`, `sqlite`, `thread` library
- qt wrapper

</details>

