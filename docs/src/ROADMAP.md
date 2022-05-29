# Hascal's Roadmap 

<details>
<summary>v1.3.x</summary>

### Language
- js backend

- lambdas :
```typescript
var mythread = thread(@(x:int,y:int){
    print(x*y)
})
```

- generate html doc from a code

### Standard Library

### Package Manager

### Other
- rebranding

</details>

<details>
<summary>v1.4.x</summary>

### Language
- rewrite compiler in hascal 
- generics
```typescript
function f<T>(x: T): T {
    return x
}
```

### Standard Library
- `thread` library

### Package Manager

### Other

</details>


<details>
<summary>v1.5.x</summary>

### Language
- classes
```typescript
class C : T {
    var foo : string
    var bar = 1

    // constructor
    C(foo: string){
        this.foo = foo
    }

    public f(x: string): string {
        return x
    }

    private f2(x: string): string {
        return x
    }

    new(foo: string): C {
        return new C(foo)
    }

    delete(foo: string): C {
        delete this.foo
        delete this.bar
    }
}
```

### Standard Library

### Package Manager

### Other

</details>
