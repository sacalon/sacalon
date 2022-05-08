# Hello World
```typescript
function main() : int {
    print("Hello World")
    return 0
}
```
Save this snippet into a file named `hello.has`. Now do: 
```
hascal hello.has
```

Congratulations - you just wrote and executed your first Hascal program!

As in many other languages (such as C++ and Rust), `main` is the entry point of your program and it should return `int` (an integer).

`print` is one of the few built-in functions. It prints the value passed to it to standard output and can be used to print multiple values:
```typescript
function main():int {
    print("Hello World", 42, true)
    return 0
}
```