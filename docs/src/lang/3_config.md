# Configure the compiler
You can use `config.json` file to configure your Hascal compiler.

The following configuration options are available:
- `filename` : your main file name, if you set it, you will no longer need to pass the file name to the compiler.
- `compiler` : your c++ compiler name(e.g : `g++`,`clang++`)
- `optimize` : optimize level(0,1,2,3)(default : no optimize, e.g: `-O2`)
- `flags` : custom flags(e.g:`["-pthread"]`)
- `c++_version` : your c++ standard(e.g:`c++17` or `c++20`),**note: c++ version must be greater than or equal to c++17 and compiler must support c++17**
- `compiler_output` : if you want to see c++ compiler output, set this to `true`
- `c++_out` : if you want to see generated c++ code, set this to `true`, the generated c++ code are in `your_filename.cc` fil.
- `only_compile` if you want only to compile and not link program, set this to `true`.
- `no_std` : if it is true, the runtime library will not link with your code(you will not be able to use builtin functions).