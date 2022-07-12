# Hascal Standard Library

- [Built-in Functions](#built-in-functions)
- [`file`](#file)
- [`os`](#os)
- [`time`](#time)
- [`math`](#math)
- [`strings`](#strings)
- [`http`](#http)
- [`random`](#random)
- [`libcinfo`](#libcinfo)
- [`termcolor`](#termcolor)
- [`crypto.sha256`](#crypto-sha256)

## Built-in functions 
- `print(...)` : Standard Hascal's print function
- `ReadStr()` : Standard Hascal's read string function
- `ReadInt()` : Standard Hascal's read integer function
- `ReadFloat()` : Standard Hascal's read float function
- `ReadBool()` : Standard Hascal's read boolean function
- `ReadChar()` : Standard Hascal's read character function
- `to_int(val:T)` : Standard Hascal's convert to integer function
- `to_float(val:T)` : Standard Hascal's convert to float function
- `to_bool(val:T)` : Standard Hascal's convert to boolean function
- `to_char(val:T)` : Standard Hascal's convert to character function
- `to_string(val:T)` : Standard Hascal's convert to string function
- `exit(exit_code:int)` : Standard Hascal's exit function
- `sizeof(T)` : Standard Hascal's sizeof function
- `typeof(T)` : Standard Hascal's typeof function
- `assert(cond:bool)` : Standard Hascal's assert function

## `file`
- `read_file(file_name:string) : string` : Read a file and return its content
- `write_file(file_name:string,content:string)` : Write a file

<!-- ### listdir(path:string) : [string]
Lists dirs,files on a path

example :
```
print(listdir("C:\\"));
``` -->

## `os`
- `os_name() : string` : Returns OS name
- `system()` : Executes a command
- `compiler_name() : string` : Returns compiler name
- `arch() : string` : Returns architecture
- `is_x86() : bool` : Returns true if architecture is x86
- `is_x64() : bool` : Returns true if architecture is x64
- `getenv(name:string) : string` : Returns environment variable

## `time`
Work with time/date

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

## `strings`
Work with strings

- `is_alpha(c:char): bool` : check if char is alphabetic
- `is_alphanum(c:char): bool` : check if char is alphanumeric
- `is_number(c:char): bool` : check if char is number
- `is_space(c:char): bool` : check if char is space
- `is_lower(c:char): bool` : check if char is lowercase
- `is_upper(c:char): bool` : check if char is uppercase
- `string_reverse(s:string): string` : reverse a string

## `http`
HTTP client-server library

- `get(url:string) : string` : get content from given url
- `post(url:string,post_data:string):string` : post content to given url
- `download(url:string,path:string):bool` : download and save a url to storage
- `upload(url:string,path:string):bool` : upload a file to a url
[See Example for http library](https://github.com/hascal/hascal/blob/main/examples/net.has)

## `random`
Random number generator

- `random_int(min:int ,sadsdfddfmax:int):int` : Returns a random integer between 0 and max

## `termcolor`
Colorize text

- `cprint(txt:string,color:string)` : print text in color
- `reset_color()` : reset color

Colors :

- `red`
- `green`
- `yellow`
- `blue`
- `magenta`
- `cyan`
- `white`
- `black`

## `crypto.sha256`
SHA256 hash

- `generate_sha256(data:string) : string` : return sha256 hash of string