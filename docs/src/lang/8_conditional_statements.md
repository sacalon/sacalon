# Conditional statements
Conditional statements are used to execute a block of code if a condition is true or false.

## If
You can use the `if` keyword to execute a block of code, if a condition is true:
```typescript
var foo : int = 1
if foo == 1 {
    print("foo is 1")
}
```

### Else
You can use the `else` keyword to execute a block of code, if a condition is false:
```typescript
var foo : int = 1
if foo == 1 {
    print("foo is 1")
} else {
    print("foo is not 1")
}
```

### Else if
You can use the `else if` statement to execute a block of code, if `else if` a condition is true:
```typescript
var foo : int = 1
if foo == 1 {
    print("foo is 1")
} else if foo == 2 {
    print("foo is 2")
} else {
    print("foo is not 1 or 2")
}
```

### `and` and `or` and `not`
You can use the `and` keyword to execute a block of code, if all conditions are true:
```typescript
var foo : int = 1
var bar : int = 2
if foo == 1 and bar == 2 {
    print("foo is 1 and bar is 2")
}
```

You can use the `or` keyword to execute a block of code, if at least one condition is true:
```typescript
var foo : int = 1
var bar : int = 2
if foo == 1 or bar == 2 {
    print("foo is 1 or bar is 2")
}
```

You can use the `not` keyword to execute a block of code, if a condition is false:
```typescript
var foo : int = 1
if not foo == 1 {
    print("foo is not 1")
}
```

## Conditional Operators
| Operator       | Description  | Example |
| :------------- | :----------: | :----------:|
|  == | Returns true if the operands are equal.   | var1 == var2 |
| !=   | Returns true if the operands are not equal. |var1 != var2|
| >  | Returns true if the left operand is greater than the right operand.  | var1 > var2 |
| >=  | Returns true if the left operand is greater than or equal to the right operand.  |var1 >= var2|
| <  | Returns true if the left operand is less than the right operand.   |var1 < var2|
| <=  | Returns true if the left operand is less than or equal to the right operand.  |var1 <= var2|
| `and`| Returns true if the left operand and right operand are true | var1 == 1 and var2 == 2|
| `or` | Returns true if the left operand or right operand are true | var1 == 1 or var2 == 2|
| `not` | Returns true if the operand are false or if the operand is true returns false | not true|
