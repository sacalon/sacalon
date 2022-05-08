# Loops
You can use the `while` keyword to execute a block of code, if a condition is true:
```typescript
var foo : int = 1
while foo == 1 {
    print("foo is 1")
    foo = 2
}
```

The `for` keyword is used to execute a block of code for a number of times:
```typescript
for i in range(0, 10) {
    print(i)
}
```
Also you can use the `for` keyword for iterating over an array:
```typescript
var foo : [int] = [1,2,3]
for i in foo {
    print(i)
}
```