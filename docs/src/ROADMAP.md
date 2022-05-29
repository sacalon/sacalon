# Hascal's Roadmap 

### Language
- js backend(`hascal2js`)

- lambdas :
```
var mythread = thread(@(1000,true){
    print("hi")
})
```

- generate html doc from a code

- generics
```typescript
function f<T>(x: T): T {
    return x
}
```

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
        return this
    }
}
```

### Standard Library
- `thread` library

### Package Manager

### Other
- redesign logo