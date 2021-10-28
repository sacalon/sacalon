# Hascal's Roadmap
- multi library import :
```
use (
   http, 
   random
)

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
@no_gc # or : @static
function add(a:int,b:int) : int {
    return a + b
}
```
