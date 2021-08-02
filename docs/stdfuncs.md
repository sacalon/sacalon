# Hascal Standard Functions

## print(...)
Standard Hascal print function

example :
```
print("Hello World");
```
## ReadStr() : string
Read string values from user

example :
```
print("What's your name ?");
var name = ReadStr();
print("Hi,",name);
```

## ReadInt() : int
Read int values from user

example :
```
print("What's your age ?");
var name = ReadInt();
print("your age :",name);
```

## ReadChar() : char
Read a character from user

example :
```
print("char :",ReadChar());
```

## ReadBool() : bool
Read a bool values from user

example :
```
print("bool :",ReadBool());
```

## ReadFloat() : float
Read float values from user

example :
```
print("float :",ReadFloat());
```

## to_int(input:auto) : int
Convert values to int

example :
```
print(to_int("123456"));
```

## to_string(input:auto) : string
Convert values to string

example :
```
print(to_string(123));
```

## to_float(input:auto) : float
Convert values to float

example :
```
print(to_float("3.14"));
```

## RemoveFile(name:string)
Removes a file

example :
```
RemoveFile("todo.txt");
```

## CloseFile(file:File)
Closes a file

example :
```
var file = File("todo.txt","w");
CloseFile(f);
```

## ReadFromFile(file:File) : string
Reads a file and returns a string value

example:
```
var myfile = File("todo.txt","r");
print(ReadFromFile(myfile));
```

## WriteToFile(file:File,data:string)
Writes a string to a file

example :
```
var file = File("todo.txt","w");

WriteToFile(file,"1-test");
CloseFile(f);
```

## listdir(path:string) : [string]
Lists dirs,files on a path

example :
```
print(listdir("C:\\"));
```

## SysPlatform() : string
Gets type of OS(win32,linux,freebsd,macos,...)

```
print(SysPlatform());
```

## ShellCommand(command:string)
Runs a shell command

example :
```
var commands = "type show_your_code.has";
ShellCommand(commands);
```

> Note: There is an important difference between ShellCommand and ExecuteCommand functions.
> The `ShellCommand` function can run only system commands, but the `ExecuteCommand` function can run any command with or without arguments.

## ExcuteCommand(command:string)
Excutes a terminal command

example :
```
var comm = "";

while true {
    print2(">>>");
    comm = ReadStr();
    ExcuteCommand(comm);
}
```

## GetYear():int,GetMonth():int,GetDay():int,GetHour():int,GetMinute():int,GetSecond():int
Gets time

example :
```
print(GetYear());
print(GetMonth());
print(GetDay());
print(GetHour());
print(GetMinute());
print(GetSecond());
```

## sin(val:float):float,cos(val:float):float,tan(val:float):float,PI(val:float):float,fmax(val:float):float,fmin(val:float):float,abs(val:float):float
Math Functions
[Example](https://github.com/hascal/hascal/tree/main/tests/math)

## exit(exit_code:int)
End program

example:
```
print("Hello");
exit(0);
print("Bye");
```
