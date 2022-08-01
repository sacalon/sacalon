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

## Passing function as parameter
To passing a function as parameter you should define a parameter in with `Function` type with following syntax :
```
Function[<function_parameter1_type>,<function_parameter2_type>,...]<return_type>
```
For example :
```typescript
function foo(func: Function[float, int]int) : int{
    
}
```
At above we defined a function with name `foo` that takes a function as its parameter and given function should has  two parameters with types `float` and `int`(respectively) and it should returns `int`.

Also we can call given function like other functions, change the `foo` function code to following code :
```typescript
function foo(func: Function[float, int]int){
    print(func(1.0,2))
}
```

Now we define a function to pass to `foo` func and must have the properties specified in the foo function(two parameters with types `int` and `float` and `int` as return type):
```typescript
function bar(a:float, b:int) : int {
    print("Hello from bar function!")
    return a + b
}
```

Now we can pass `bar` function to `foo` function as parameter :
```typescript 
foo(bar)
```

Output :
```
Hello from bar function!
3
```