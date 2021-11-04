# Functions
A Hascal function is a block of code designed to perform a particular task.
A Hascal function is executed when "something" invokes it (calls it).

syntax :
```
function <name>(<name>:<type>,...):<return_type> {
  <statements>
}
```
**NOTE:** if your function , don't return any thing ,you can use following syntax.
```
function <name>(<name>:<type>,...){
  <statements>
}
# example :
function foo(x:int){
  print(x)
}
```

**NOTE:** if your function , don't get any value , you can use following syntax.
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
<function name>(<arguments>)
```

## return a value in function
for return a value , look following example :
```
function foo() :int{
  return 1
}
print(foo())# output : 1
```
