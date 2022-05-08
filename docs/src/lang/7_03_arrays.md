# Arrays
Arrays are collections of data elements of the same type. They can be represented by a list of elements surrounded by brackets. The elements can be accessed by appending an index (starting with 0) in brackets to the array variable:

Arrays declare like following:
```typescript
var foo : [int] = [1,2,3]
var bar : [string] = ["Hello", "World"]
```

You can use the `[]` operator to access an element in an array:
```typescript
var foo : [int] = [1,2,3]
print(foo[1]) // 2
```

And you can assign a value to an array element:
```typescript
var foo : [int] = [1,2,3]
foo[1] = 4
print(foo[1]) // 4
```

With `append` built-in function you can append an element to an array:
```typescript
var foo : [int] = [1,2,3]
foo.append(4)
print(foo[3]) // 4
```

And you can get the length of an array with the `len` built-in function:
```typescript
var foo : [int] = [1,2,3]
print(len(foo)) // 3
```