# Package Manager
Hascal has a built-in package manager that allows you to install packages from the a git repository.

## Installing a package
To get and install a package, you can use the `get` command :
```
hascal get <git url> <package name>
```
- `<git url>` is the url of the git repository
- `<package name>` is the name of the package(optional, recommended, default is the url)

Note: If you don't specify the package name, you should import it like this :
```typescript
use github.com.foo.bar
```


## Updating a package
To update a package, you can use the `update` command :
```
hascal update <package name ot git url>
```
