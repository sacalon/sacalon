# `path`
Working with pathes.

## `path_normalize(path:string):string`
Normalize a path.

Example :
```typescript
print(path_normalize("/home/myapp/files/////config"))
```

```
// Output(*Nix) :
/home/myapp/files/config

// Output(Windows):
/home\myapp\files\config
```

## `path_join(path_a:string, path_b:string):string`
Join `path_a` and `path_b` pathes.

Example :
```typescript
print(path_normalize("/home/myapp","files/config"))
```

```
// Output:
/home/myapp/files/config
```
