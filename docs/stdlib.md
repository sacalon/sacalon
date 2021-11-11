# Hascal Standard Library

- [Built-in Functions](#built-in-functions)
- [`file`](#file)
- [`os`](#os)
- [`time`](#time)
- [`math`](#math)

## Built-in functions 

### print(...)
Standard Hascal's print function

example :
```
print("Hello World");
```

### ReadStr() : string
Read string values from user

example :
```
print("What's your name ?");
var name = ReadStr();
print("Hi,",name);
```

### ReadInt() : int
Read int values from user

example :
```
print("What's your age ?");
var name = ReadInt();
print("your age :",name);
```

### ReadChar() : char
Read a character from user

example :
```
print("char :",ReadChar());
```

### ReadBool() : bool
Read a bool values from user

example :
```
print("bool :",ReadBool());
```

### ReadFloat() : float
Read float values from user

example :
```
print("float :",ReadFloat());
```

### to_int(input:Type) : int
Convert values to int

example :
```
print(to_int("123456"));
```

### to_string(input:Type) : string
Convert values to string

example :
```
print(to_string(123));
```

### to_float(input:Type) : float
Convert values to float

example :
```
print(to_float("3.14"));
```

### exit(exit_code:int)
End program

example:
```
print("Hello");
exit(0);
print("Bye");
```

## `file`

### read_file(file_name:string) : string
Read from file

example :
```
var content : string = read_file("todo.txt");
```

### write_file(path:string,text:string) : bool
Write to file

example :
```
write_file("todo.txt","- Going to gym")
```

<!-- ### listdir(path:string) : [string]
Lists dirs,files on a path

example :
```
print(listdir("C:\\"));
``` -->

## `os`

### os_name() : string
Gets type of OS(win32,linux,freebsd,macos,...)

```
print(os_name());
```

### system(command:string)
Excutes a terminal command

example :
```
var comm = "";

while true {
    print2("MyCMD>>>");
    comm = ReadStr();
    system(comm);
}
```

## `time`

- `get_year():int` : Get current year
- `get_month():int` : Get current month
- `get_day():int` : Get current day
- `get_hour():int` : Get current hour
- `get_minute():int` : Get current minute
- `get_second():int` : Get current second


## `math`
Math Functions
- `sin(val:float):float` : Returns sine of x
- `cos(val:float):float` : Returns cosine of x
- `tan(val:float):float` : Returns tangent of x
- `PI : float` : PI number
- `fmax(x:float,y:float):float` : Returns the larger of x and y(floating point). 
- `fmin(x:float,y:float):float` : Returns the smaller of x and y(floating point). 
- `max(x:int,y:int):int` : Returns the larger of x and y. 
- `min(x:int,y:int):int` : Returns the smaller of x and y. 
- `abs(x:float):float` : Calculates the absolute value of a number. 