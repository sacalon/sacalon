# `math`
Math library has properties and methods for mathematical constants and functions

**NOTE**:**All functions that return and give `double` type, also can return and give `float` type**
----

## Trigonometric ratios

## `sin(x:double):double`
Returns sine of x.

## `cos(x:double):double`
Returns cosine of x.

## `tan(x:double):double`
Returns tangent of x.

## `asin(x:double):double`
Returns arc sine of x.

## `acos(x:double):double`
Returns arx cosine of x.

## `atan(x:double):double`
Returns arc tangent of x.

## `asin(x:double):double`
Returns arc sine of x.

## `acos(x:double):double`
Returns arc cosine of x.

## `atan(x:double):double`
Returns arc tangent of x.

## `atan2(y:double,x:double):double`
Returns the principal value of the arc tangent of y/x, expressed in radians.

## `sinh(x:double):double`
Returns hyperbolic sine of x.

## `acos(x:double):double`
Returns hyperbolic cosine of x.

## `tan(x:double):double`
Returns hyperbolic tangent of x.

## `atan(x:double):double`
Returns area hyperbolic tangent of x.

## `asin(x:double):double`
Returns area hyperbolic sine of x.

## `acos(x:double):double`
Returns area hyperbolic cosine of x.

## `atan(x:double):double`
Returns arc tangent of x.

----

## Exponential and logarithmic functions

## `exp(x:double):double`
Returns the base-e exponential function of x, which is e raised to the power x: e^x.

## `exp2(x:double):double`
Returns the base-2 exponential function of x, which is 2 raised to the power x: 2^x.

## `frexp(x:double,exp:int^): double`
Breaks the floating point number x into its binary significand (a floating point with an absolute value between 0.5(included) and 1.0(excluded)) and an integral exponent for 2, such that:

```
x = significand * (2  ^ exponent)
```

The exponent is stored in the location pointed by exp, and the significand is the value returned by the function.

If x is zero, both parts (significand and exponent) are zero.
If x is negative, the significand returned by this function is negative.

## `ldexp(x:float|dobule,exp:int): float|dobule`
Returns the result of multiplying x (the significand) by 2 raised to the power of exp (the exponent).

## `log(x:float|dobule):float|dobule`
Returns the natural logarithm of x.

## `log10(x:float|dobule):float|dobule`
Returns the common (base-10) logarithm of x.

## `log2(x:float|dobule):float|dobule`
Returns the binary (base-2) logarithm of x.

----

## Power functions

## `pow(base:double,exponent:double): double`
Returns base raised to the power exponent.

## `sqrt(x:double):double`
Returns the square root of x.

----

## Rounding and remainder functions

## `ceil(x:double):double`
Rounds x upward, returning the smallest integral value that is not less than x.

## `floor(x:double):double`
Rounds x downward, returning the largest integral value that is not greater than x.

## `fmod(x:double):double`
Returns the floating-point remainder of numer/denom (rounded towards zero):

fmod = numer - tquot * denom

Where tquot is the truncated (i.e., rounded towards zero) result of: numer/denom.

## `round(x:double):double`
Roundes x to nearest ineger value

----

## Minimum, maximum, difference functions

## `fmax(x:double,y:double):double`
Returns the larger of its arguments: either x or y(floating point).

## `fmin(x:double,y:double):double`
Returns the smaller of its arguments: either x or y(floating point).

## `max(x:int,y:int):int`
Returns the larger of x and y.

## `min(x:int,y:int):int`
Returns the smaller of x and y. 

## `fdim(x:double,y:double)`
Returns the positive difference between x and y.

----

## Other functions and constants

## `const PI : double`
PI number.

## `NaN():double`
Returns generic NaN(Not-A-Number) value.

## `fabs(x:double):double`
Calculates the absolute value of x(floating point).

## `abs(x:int):int`
Calculates the absolute value of x(ineger).
