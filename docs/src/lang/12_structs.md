# Structures
Structures are a way to group data together. You can declare a structure using the `struct` keyword:
```typescript
struct Color {
    var r : int
    var g : int
    var b : int
    var name = "Anything..." // optional
}
```
> Note: Declaring a structure member without a type will make it optional.

After declaring a structure, you can create an instance of it:
```typescript
var red = Color(255,0,0)
```

For accessing the fields of a structure, you should use the `.` operator:
```typescript
var red = Color(255,0,0)
print(red.r)
print(red.g)
print(red.b)
print(red.name)
```

## Structures as return values
You can return a structure from a function:
```typescript
function foo() : Color {
    return Color(1,2,3)
}
```

## Structures as arguments
You can pass a structure as an argument to a function:
```typescript
function foo(c:Color) {
    print(c.r)
    print(c.g)
    print(c.b)
    print(c.name)
}
```

## Structure inheritance
You can inherit a structure from another structure with `:` operator after the structure name:
```typescript
struct RGB : Color {
    
}
```

And you can access the fields of the inherited structure:
```typescript
var foo : RGB = RGB(1,2,3)
print(foo.r,foo.g,foo.b)
   
var bar = RGB(255,0,0,"AColor")
```