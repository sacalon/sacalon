# Variables

Variables are like containers in which values can be inserted or changed.

variable defining:

```hascal
var name [: type [= value]];
```

- `name`: your variable name  
> **NOTE:** names should not start with a number,
By compiling this code, you will receive an error:
```hascal
var 6Apple : int;
```

- `type`: your variable type
- `value`: your variable value

example :
```hascal
var myvar : string ;
var my_var : int ;
var _myvar : float;
```

### Variable assignment
Do the following to give a value to the variable :
```
name = value ;
```

example :
```
var x : int;
x = 14 ;
```

You can not assign a value  to a variable as opposed to the original type ,this code have error :
```
var myInt : int;
myint = 1.1; # error
```

# Constants
Constant(const) is a type qualifier a keyword applied to a data type that indicates that the data is read only(wikipedia).

for example :
```
const MyConst = "MyName"; # or : let MyConst = "MyName";
print(MyConst); # output : MyName
```
**NOTE:** You cannot change the const values.
for example (compiler return an error):
```
const PI = 3.14 ; # or : let PI = 3.14 ;
PI = 3.1415 ; # error
```
