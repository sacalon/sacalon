# Builtin Functions
Hascal builtin functions is a part of Hascal's runtime library that link to any Hascal program.

## `print(...)`
Standard Hascal's print function.

Example :
```typescript
print("Hello",1,1.0,'a',[1,2,3,4])
```

## `ReadStr() : string`
Standard Hascal's read string function

## `ReadInt() : int`
Standard Hascal's read integer function

## `ReadFloat() : float`
Standard Hascal's read float function

## `ReadBool() : bool`
Standard Hascal's read boolean function

## `ReadChar() : char`
Standard Hascal's read character function

## `ReadStr(text:string) : string`
Standard Hascal's read string function with printing a prompt.

## `ReadInt(text:string) : int`
Standard Hascal's read integer function with printing a prompt.

## `ReadFloat(text:string) : float`
Standard Hascal's read float function with printing a prompt.

## `ReadBool(text:string) : bool`
Standard Hascal's read boolean function with printing a prompt.

## `ReadChar(text:string) : char`
Standard Hascal's read character function with printing a prompt.

## `exit(exit_code:int)`
Exit program with an `exit_code`.

## `sizeof(T) : int`
Get sizeof a type or expression.

If input value is a type, it will return the amount of memory is allocated to that data types.
Else if input value is a expression, it will return size of expression.

## `typeof(T) : string`
Get name of a type.

Example :
```typescript
print(typeof(int)) // int
print(typeof(MyStructType)) // MyStructType
```
## `assert(cond:bool) : bool`
The `assert` function is used when debugging code, `assert` lets you test if a condition in your code returns `true`, if not, the program will be exit.

Example :
```typescript
var foo = 1
var bar = 2

assert(foo == bar)
```