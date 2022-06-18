# Strings
Strings are a sequence of characters. You can declare a string using the `string` keyword:
```typescript
var foo : string = "Hello World"
```

You can use the `+` operator to concatenate strings:
```typescript
var foo : string = "Hello" + " World"
```

And you can use the `[]` operator to access a character in a string:
```typescript
var foo : string = "Hello"
print(foo[1]) // 'e'
```
> Note: type of accessed character is `char`
> Note: the first character in a string is at index 0.


With `len` function you can get the length of a string:
```typescript
var foo : string = "Hello"
print(len(foo)) // 5
```
> Note: `len` function is a built-in function.

#### Escape sequences
You can use escape sequences to print special characters:
```typescript
var foo : string = "Hello\tWorld"
print(foo) // Hello    World
```

The following escape sequences are supported:
- `\n` : newline
- `\t` : tab
- `\r` : carriage return
- `\\` : backslash
- `\'` : single quote
- `\"` : double quote
- `\?` : question mark
- `\a` : bell
- `\b` : backspace
- `\f` : form feed
- `\v` : vertical tab
- `\0` : null character
- `\x____` : hexadecimal character
- `\u____` : unicode character
- `\U____` : unicode character
- `\_____` : arbitrary octal value 

Note: `_____` means you should specify the id of the character you want to print.

#### Reverse a string
You can reverse a string by using the `string_reverse` function in the `strings` package:
```typescript
use strings

function main() {
    var foo : string = "Hello World"
    print(string_reverse(foo)) // dlroW olleH
}