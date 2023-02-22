# `functional`
Functional programming library for Hascal.

## `plus(a:float, b:float):float`
Additiona function.

## `minus(a:float, b:float):float`
Subtraction functions.

## `multiplies(a:float, b:float):float`
Multiplication function.

## `divide(a:float, b:float):float`
Division function

## `negate(a:float): float`
Negative function.

## `equals(a:float, b:float): bool`
equality comparison.

## `lessThan(a:float, b:float): bool`
less-than inequality comparison.

## `greaterThan(a:float, b:float): bool`
greater-than inequality comparison.

## `lessThanEqual(a:float, b:float): bool`
less-than-or-equal-to comparison.

## `greaterThanEqual(a:float, b:float): bool`
greater-than-or-equal-to comparison.

## `notEqual(a:float, b:float): bool`
non-equality comparison.

## `and_(a:bool, b:bool): bool`
Implements `and` operator.

Example(without `functional`) :
```typescript
if a == b and a == c {
    // ...
}
```

Example(with `functional`) :
```typescript
if(and_(a == b,a == c)) {
    // ...
}
```

## `or_(a:bool, b:bool): bool`
Implements `or` operator.

Example(without `functional`) :
```typescript
if a == b or a == c {
    // ...
}
```

Example(with `functional`) :
```typescript
if(or_(a == b,a == c)) {
    // ...
}
```

## `not_(a:bool): bool`
Return negation of `a`.

## `ifThenElse(a:bool, b:float, c:float): float`
If `a` is `true`, returns `b`, else `c`.

## `mod(a:float, b:float): float`
Modulus function.
