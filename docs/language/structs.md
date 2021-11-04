# Struct(Structure)
The structure is a user-defined data type in Hascal, which is used to store a collection of different kinds of data. 

syntax :
```
struct <name> {
  var <name> : <type> 
  ...
}
```

example :
```
struct Student {
  var name : string
  var age : int 
}
```

## Defining a struct
example :
```
struct Student{
    var name : string
    var age : int
}

var John0 = Student() 
```

## Access to struct fields
example : 
```
struct Student{
    var name : string
    var age : int
}

var John0 = Student() 
John0.name = "John0"
print(John0.name)
```

## Array fields in struct
example :
```
struct Student {
    var my_brothers : [string]
}

var me : Student 
me.my_brothers[0] = "Ali" 

print(me.my_brothers[0]) # output : Ali
```

## struct as function argument
example :
```
struct Student{
    var name : string 
}
function foo(obj:Student){
    print(obj.name)
}

var bar = Student("john")

foo(bar)
```
