# Hello World!
Now that you have successfully installed Hascal, let's write our first program with it. You will write a program that prints `Hello World!` on the terminal.

## Creating a project directory
You can wite your hascal programs every where but We suggest that you create a directory for your project.


First create a directory in your home directory(or anywhere else):
```
mkdir hello_world
cd hello_wrold
```

## Writing the code
Next make a new file and name it `main.has`. Hascal files should end with `.has` extension.

Now open your code editor(If you are using `vscode` install hascal extension for better coding from [this link](https://github.com/hascal/vscode)) and write following code in `main.has` :
```typescript
function main() : int {
    print("Hello World!")
    return 0
}
```
Save the file, and back to terminal and enter following command to build your program :
```
hascal main.has
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

Congratulations - you just wrote and executed your first Hascal program!

## Reviewing the code
Let's review the our simple program. Here's the first piece of the program :
```typescript
function main() : int {
    
}
```
These lines defines a function that returns an integer number. The `main` function is the entry point of your program and it always should return `int`(an integer), if there were parameters, they would go inside the parentheses, `()`.

Also, note function statements should be in `{}` and you write function codes inside `{}`.

Inside the `main` function is the following code :
```typescript
print("Hello World!")
```

This code print the passed arguments, you can pass more parameters :
```typescript
print("Hello World!",42,3.14)
```

After the calling `print` command is following statemetn :
```typescript
return 0
```
It returns `0` at end of the function, every function that returns a value(declared with `:` after `()` in function declaration) should return a value with mentioned type. 

Returning the `0` value in main function tell the OS that your program executed successfully.