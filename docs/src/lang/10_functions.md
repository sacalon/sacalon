# Functions
Functions are a way to group code that can be called to perform a specific task. You can declare a function using the `function` keyword:
```typescript
function foo() {
    print("Hello World")
}
```

Also your function block should be outside of a function.

Your function can have parameters and return a value. You can declare parameters and return type, like variable declarations:
```typescript
function add(x:int,y:int): int {
    return x + y
}
```
In the example above, `x` and `y` are parameters and their type(`int`) is your return type.

> Note: you can use `?` to make a parameter nullable.

## Calling a function
You can call a function by using the function name followed by parentheses:
```typescript
foo()
```
If you want to pass some arguments to your function, you can use them in the parentheses(separate with `,`):
```typescript
foo(1,2,3)
```

Also you can assign the return value of a function to a variable:
```typescript
var foo : int = add(1,2)
```

## Function overloading
You can overload functions by defining a new function and changing the number of parameters or the type of parameters or return type of function :
```typescript
function add(x:int,y:int,z:int): int {
    return x + y + z
}

// overloading function `add`
function add(x:int,y:int){
    print(x + y)
}

function main(): int {
    print(add(1,2))
    print(add(1,2,3))
}
```

## Passing function as argument
You can pass a function as an argument to another function:
```typescript
function runner(func: Function[int, int]int) : int{
    return func(1,2)
}

function add(a:int, b:int) : int {
    return a+b
}

function main():int {
    print(runner(add))
    return 0
}
```
In the example above, `runner` is a function that takes a function as an argument and returns the return value of the given function.
