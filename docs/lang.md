# Learn Hascal in 15 minutes
```nim
# import math library from stdlib
use math

# DataTypes :
# - char
# - string
# - int 
# - float 
# - bool 

# declare a variable
var x : int = 1

# declare an array
var names : [string] = ["ali","mohammad"]

# declare a const
const xx : int = 1
const pi = 3.14

# define a function
function add(x:int,y:int) : int {
    return x + y
}

# define a struct
struct Student {
    var name : string
    var age : int
}

# main function
function main(argv:[string]) : int {
    # print values
    print("Hi!",1,2)

    # if statement
    if x == 1 {
        print(1)
    }else if x == 1 {
        print(2)
    }else {
        print(3)
    }

    # for statement
    for x = 1 to 10 {
        print(x)
    }

    # while statement
    while x < 100 {
        x = x + 1
        print(x)
    }

    # call a function
    my_func("arg 1",1)
    return 0
}

```
