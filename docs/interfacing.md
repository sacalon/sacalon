# Interfacing to C/C++
You can use C and C++ in Hascal.
For example, we want to write a function for print abs of a value in c++ and use it in hascal, first create a folder with `cpp` name and create `absprint.cc` and `absprint.hpp` in created folder.

`absprint.cc` :
```c++
void absprint(int a){
   std::cout << abs(a);
}
```
For use `abs()` function we should import it from c++ stdlib, for this purpose import it in `absprint.hpp` :
`absprint.hpp`
```c++
#include <cmath>
```
Now can import this code in hascal, write this code in root folder of your project:
```typescript
local use cpp.absprint
function absprint(a:int) : int

function main() : int {
   absprint(-68) # output : 68
}
```
You can write inline function,structs,... defines, in an external hascal file and import it in main file :
`absprint.has` :
```typescript
local use cpp.absprint

function absprint(a:int) : int
```
`main.has` :
```
local use absprint

function main() : int {
   absprint(-68) # output : 68
}
```
