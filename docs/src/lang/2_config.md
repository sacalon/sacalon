# Configure the compiler
You can use `config.json` file to configure your Hascal compiler.

The following configuration options are available:
- `compiler` : your c++ compiler name(e.g : `g++`,`clang++`)
- `optimize` : optimize level(0,1,2,3)(default : no optimize)
- `flags` : custom flags(e.g:`["-pthread"]`)
- `no_check_g++` : if you don't use g++, set this to `true`
- `c++_version` : your c++ standard(e.g:`c++17` or `c++20`),**note: c++ version must be greater than or equal to c++17 and compiler must support c++17**
- `g++_out` : if you want to see g++ output, set this to `true`
- `c++_out` : if you want to see generated c++ code, set this to `true`
- `only_compile` if you want to only compile and not link program, set this to `true`

example :

```json
{
    "compiler":"g++",
    "optimize":"-O2",
    "flags":["-pthread"],
    "no_check_g++":1,
    "c++_version":"c++17",
    "g++_out":1,
    "c++_out":1
}
```