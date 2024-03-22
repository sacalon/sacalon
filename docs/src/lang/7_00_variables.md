# Variables
A variable is a named storage for a value. Variables are declared using the `var` keyword :
```typescript
var foo : int = 1
```

Also you can declare a variable without type, in this case, the type will be inferred by the value assigned to it:
```typescript
var foo = 1
```

### Non nullable and nullable
Null safety is a feature that allows you to declare that a variable can be null or not null, and Sacalon uses this feature to make sure that your code is safe.

Sacalon's variables and constants are non-nullable by default that means that they cannot be null(`NULL`) and you can't assign `NULL` to them and **you should assign a value to them when you declare them**.

```typescript
var foo : int = 1 // non-nullable
var foo_error : int // error : non-nullable variable must be assigned a value
```

But you can make variables and constants nullable by adding `?` to their type:

```typescript
var bar : int? = 1 // nullable
```

so you can use `NULL` to set a variable to null :

```typescript
bar = NULL // ok
```


## Pointers
Pointers are a way to access the memory address of a variable. You can declare a pointer using the `^` operator after the type:

```typescript
var foo : int^?
```
***NOTE:*** pointers are non-nullable by default, use `?` to make it nullable:

You use cast to assign a value to a pointer:
```typescript
foo = (int^)1
```

Finally, you can use the `^` operator to access the value stored in a pointer:
```typescript
var foo : int^ = (int^)1
print(^foo) // 1
```
**NOTE**: We recommend you to always allocate pointers with `new` keyword and deallocate with `delete` keyword, for more information go to [Memory management chapter](13_memory_management.md).

NOTE: Currently only one level of pointers are supported.

## Static variables
Static variables are variables that are declared outside of a function and are accessible from anywhere in the program.

Static variables are declared using the `static` keyword before the type:
```typescript
var foo : static int = 1
```