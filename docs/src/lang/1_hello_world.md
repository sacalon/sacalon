# Hello World!
Now that you have successfully installed Sacalon, let's write our first program with it. You will write a program that prints `Hello World!` on the terminal.

## Creating a project directory
You can write your Sacalon programs every where but, we suggest that you create a directory for your project.


At first, create a directory in your home directory(or anywhere else):
```
mkdir hello_world
cd hello_wrold
```

## Writing the code
Next make a new file and name it `main.sa`. Sacalon files should end with `.sa` extension.

Now open your code editor (If you are using `vscode` install sacalon extension for better coding from [this link](https://github.com/sacalon-lang/vscode)) and write the following code in `main.sa` :
```typescript
function main() : int {
    print("Hello World!")
    return 0
}
```
Save the file, and return to the terminal and enter the following command to build your program :
```
sacalon main.sa
```

Now run the generated excutable file :
```
$ ./main
Hello World!
```
On Windows you should use `.\main.exe` instead of `./main` :
```
$ .\main.exe
Hello World!
```

Congratulations - you just wrote and executed your first Sacalon program!

## Reviewing the code
Let's review our simple program. Here's the first piece of the program:
```typescript
function main() : int {
    
}
```
These lines define a function that returns an integer number. The `main` function is the entry point of your program and it should always return `int`(an integer). If there were parameters, they would go inside the parentheses, `()`.

Also, note that function statements should be in `{}` and you can write function codes inside `{}`.

Inside the `main` function is the following code :
```typescript
print("Hello World!")
```

This code print the passed arguments, you can pass more parameters :
```typescript
print("Hello World!",42,3.14)
```

After the calling `print` command, there is the following statement :
```typescript
return 0
```
It returns `0` at the end of the function, every function that returns a value(declared with `:` after `()` in a function declaration) should return a value corresponding to the type.

Returning the `0` value in main function tell the OS that your program has executed successfully.