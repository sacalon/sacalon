# Hascal's Roadmap 

### Language
- js backend
- lambdas :
```typescript
var mythread = thread(function(x:int,y:int){
    print(x*y)
})
```
- generate html doc from a code
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

    // allocator
    __new__(foo: string): C {
        return new C(foo)
    }

    // deallocator
    __delete__(foo: string): C {
        delete this.foo
        delete this.bar
    }
}
```
- generics [#26](https://github.com/hascal/hascal/issues/26)s
- rewrite compiler in hascal 
- const correctness

### Standard Library
- `thread` library

### Package Manager
