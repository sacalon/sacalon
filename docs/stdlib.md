# Hascal Standard Library

- [Built-in Functions]()
- [`file`]()
- [`os`]()
- [`time`]()
- [`math`]()

## Built-in functions 

### print(...)
Standard Hascal print function

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

### to_int(input:auto) : int
Convert values to int

example :
```
print(to_int("123456"));
```

### to_string(input:auto) : string
Convert values to string

example :
```
print(to_string(123));
```

### to_float(input:auto) : float
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

### RemoveFile(name:string)
Removes a file

example :
```
RemoveFile("todo.txt");
```

### CloseFile(file:File)
Closes a file

example :
```
var file = File("todo.txt","w");
CloseFile(f);
```

### ReadFromFile(file:File) : string
Reads a file and returns a string value

example:
```
var myfile = File("todo.txt","r");
print(ReadFromFile(myfile));
```

### WriteToFile(file:File,data:string)
Writes a string to a file

example :
```
var file = File("todo.txt","w");

WriteToFile(file,"1-test");
CloseFile(f);
```

### listdir(path:string) : [string]
Lists dirs,files on a path

example :
```
print(listdir("C:\\"));
```

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

- `GetYear():int` : Get year
- `GetMonth():int` : Get month
- `GetDay():int` : Get day
- `GetHour():int` : Get hour
- `GetMinute():int` : Get minute
- `GetSecond():int` : Get second


## `math`
Math Functions
- `sin(val:float):float` : Returns sine of x
- `cos(val:float):float` : Returns cosine of x
- `tan(val:float):float` : Returns tangent of x
- `PI : float` : PI number
- `fmax(x:float,y:float):float` : Returns the larger of x and y. 
- `fmin(val:float):float` : Returns the smaller of x and y. 
- `abs(x:float):float` : Calculates the absolute value of a number. 