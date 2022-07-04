# Importing & Creating modules
A module is a package of code that can be imported into another module to use its code.

## Importing a module
You can use other modules by importing them. You can import a module by using the `use` keyword:
```typescript
use os

function main() : int {
   system("start http://www.google.com")
   return 0
}
```

### Importing multiple modules
You can import multiple modules by using the `use` keyword and separating the module names with a comma:
```typescript
use os, math, conv
```

For importing a submodule of a module, you can use the `.` operator:
```typescript
use crypto.sha256
```

## Creating a module
For creating a module, you can create a file with the same name as the module and with the extension `.has` and put the module code inside it:

`add.has`:

```typescript
function add(x:int, y:int) : int {
    return x + y
}
```

`main.has`:
```typescript
use add

function main() : int {
    print(add(1,2))
    return 0
}
```

#### Creating foldered modules
Module files can be placed in a folder, for creating a foldered module you should first create the folder and then create the `_.has` file inside it.

The `_.has` file is the main file of the module and compiler will look for it.
You can also import submodules in `_.has` file.

> Note: Any submodule that is not imported in `_.has` file will be ignored.
> Note: Any submodule can have other submodules.
