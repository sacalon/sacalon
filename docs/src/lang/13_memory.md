# Memory management
Memory management is a way to manage the memory of your program. Hascall use manual memory management because this manual memory management is used in most performance-critical applications like games,OSes, embedded systems, etc.

Hascal uses `new` and `delete` keywords to manage memory, manually.

## Allocation
For allocating memory, you should use the `new` keyword. Note that type of the allocated memory should be pointer or reference type :
```typescript
var foo : int^ = new int(1)
```

For easily declaring and allocating memory, use `var <name> = new <type>(<args...>)` statement, like this:
```typescript
var foo = new int(1)
```

## Reallocation
For reallocating memory and assigning the new value to the pointer, use `<pointer> = new <type>(<args...>)` statement, like this:
```typescript
var foo : int^ = new int(1) // allocate memory
foo = new int(2) // reallocate memory and assign new value
```

## Deallocation
For deallocating memory, you should use the `delete` keyword and pass the pointer to the memory that you want to deallocate:
```typescript
delete foo
```



## Accessing memory
Like pointers, you can access the allocated memory value with the `^` operator:
```typescript
var foo : int^ = new int(1)
print(^foo)
```

## Critical notes
- <span style="color:red">Don't forget to use the `delete` keyword at end of scope and before the end of the program.</span>.
> In future, we will add a feature to show warnings when you forget to use the `delete` keyword.

- **You can't deallocate memory that you haven't allocated it without `new` keyword.**

- **You can allocate, not allocated pointers**:
```typescript
var foo : int^?
foo = new int(1)
```