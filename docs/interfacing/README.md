# Interfacing to D\C\C++\Obj-C
You can use d, c, c++ and objective c in hascal.
For example, we want to write a function for print abs of a value in d and use it in hascal, first create a folder with `d` name and create `absprint.d` and `absprint.h` in created folder.

`absprint.d` :
```d
int absprint(int a){
   return writeln(abs(a));
}
```
For use `abs()` function we should import it from d stdlib, for this purpose import it in `absprint.h` :
`absprint.h`
```h
import math : abs ;
```
Now can import this code in hascal, write this code in root folder of your project:
```typescript
local use d.absprint
function absprint(a:int) : int

function main() : int {
   absprint(-68) # output : 68
}
```
You can write inline function,structs,... defines, in an external hascal file and import it in main file :
`absprint.has` :
```typescript
local use d.absprint

function absprint(a:int) : int
```
`main.has` :
```
local use abaprint

function main() : int {
   absprint(-68) # output : 68
}
```

## Use other languages in hascal
You can extern c\c++\obj-c in d and use it in hascal.

`foo.d` :
```
extern(C) {
   // put your c code here
}
