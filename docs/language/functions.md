# Functions
A Hascal function is a block of code designed to perform a particular task.
A Hascal function is executed when "something" invokes it (calls it).

syntax :
```
function <name>(<name>:<type>,...):<return_type> {
  <statements>
}
```

Function's syntax without value :
```
function <name>(<name>:<type>,...){
  <statements>
}
# example :
function foo(x:int){
  print(x)
}
```

Function's syntax without parameters :
```
function <name>(){
  <statements>
}
# or :
function <name> {
  <statements>
}

# example :
function foo(){
  print("Hello")
}
```

## Call a function
for call and excute a function , use this syntax :
```
<function_name>(<arguments>)
```

## return a value in function
```
function foo() :int{
  return 1
}
print(foo())# output : 1
```
