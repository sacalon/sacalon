# Condition operators
| Operator       | Description  | Example |
| :------------- | :----------: | :----------:|
|  == | Returns true if the operands are equal.   | var1 == var2 |
| !=   | Returns true if the operands are not equal. |var1 != var2|
| >  | Returns true if the left operand is greater than the right operand.  | var1 > var2 |
| >=  | Returns true if the left operand is greater than or equal to the right operand.  |var1 >= var2|
| <  | Returns true if the left operand is less than the right operand.   |var1 < var2|
| <=  | Returns true if the left operand is less than or equal to the right operand.  |var1 <= var2|

# If,else,else if statement
- Use `if` to specify a block of code to be executed, if a specified condition is true
- Use `else` to specify a block of code to be executed, if the same condition is false
- Use `else if` to specify a new condition to test, if the first condition is false



## if
syntax :
```
if <condition> {
  <statements>
}
```

example :
```
var x = 1
if x == 1 {
  print("x==1")
}
```

## if else
syntax :
```
if <condition> {
  <statements>
}else {
  <statements>
}
```

example :
```
var foo = 2
if foo == 1{
  print("foo==1")
}else {
  print("foo!=1")
}
```


## if else if
syntax :
```
if <condition> {
  <statements>
}else if <condition> {
  <statements>
}
```

example :
```
var foo = 2
if foo == 1{
  print("foo==1")
}else if foo == 2{
  print("foo!=2")
}
```

# Loops
Loops are handy, if you want to run the same code over and over again, each time with a different value.

## for loop

syntax :
```
for <name> = <expr> to <expr> {
  <statements>
}
# or :
for <name> = <expr> downto <expr> {
  <statements>
}
```

example :
```
var x = 1

for x = 1 to 10 {
	print(x)
}

print("----")

x = 100
for x = 100 downto 0 {
	print(x)
}
```

## while loop
syntax :
```
while <condition> {
  <statements>
}
```
example :
```
var x = 1

while x<=100 {
	print("\n",x)
	x = x + 1
}
```
