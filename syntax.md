# Hascal Syntax Example

### hello world :
```dart
print("Hello World");
```
### variables :
```dart
var x = 1;
var str = "Hascal";
var pi = 3.14 ;
var testBool = true;
var ch = 'h';
```
or:
```dart
var x : int ;
x = 1 ;
var str : string;
str = "Hascal";
var pi : float ;
pi = 3.14;
var testBool : bool;
testBool = true;
var ch : char;
ch = 'h';
```
### arrays:
```dart
var ages : [int]= [12,13,14,15];
var strs : [string] = ["hello" , "bye"];
var fls : [float] = [1.0,1.1,1.3];
var bls : [bool]= [true , false,false];
var chs : [char] = ['h','a','s','c','a','l']; 

var names = ["ali","mohammad"];
```
### read values :
```dart
var x = 0;
x = ReadInt();

var str = "";
str = ReadStr();

var fl = 0.0;
fl = ReadFloat();
```
### comments :
```dart
# this is a single line comment
```

## Conditionals

### if...else :
```dart
var x = 1;
if x == 1 {
  print("x==1");
} else {
  print("x!=1");
}

```

## Loops

### for loop :
```dart
var x = 0;
for x = 0 to 10 {
  print(x);
}
```

or :
```dart
var x = 0;
for x = 100 downto 1 {
  print(x);
}
```
### while loop :
```dart
var x = 1;
while x == 1 {
  print("loop");
}

```

## Advanced data types

### functions :
```dart
function sayHello() {
  print("hello");
}

function ret(): string {
  return "hello";
}

function ret2(ss:string): string {
  print(ss);
}
```
### structs
```dart
struct Student {
  var name :string;
  var age :int;
}

var John = Student("john",36);

print(John.name);
# output : john
```

## Modules
### use modules:
```dart
use your_module_name;
```
for example :
```dart
use hascal.core;
```

use local hascal module(library):
```dart
local use mylib;
```
