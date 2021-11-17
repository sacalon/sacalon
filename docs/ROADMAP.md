# Hascal's Roadmap 

<details>
<summary>v1.3.x</summary>

### Base
- C++ in back-end
- garbage collection and Rust-like memory management

### Language
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

- lambdas :
```
var mythread = thread(@(1000,true){
    print("hi")
})
```

- immutable variables
```
let x : int = 1
```

- function decorators :
```
@static
function add(a:int,b:int) : int {
    return a + b
}
```
- `@no_mm` decorator for manual memory management
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
- `panic` based error management
- linker flag option
    
### Standard Library
- `json`, `sqlite` library

</details>

