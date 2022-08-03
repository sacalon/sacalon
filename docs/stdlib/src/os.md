# `os`
Interaction with OS.

## `os_name() : string`
Returns OS name

| OS(Platfrom)      | `os_name()` output  | 
| :------------- | :----------: | 
| Windows 32-Bit | `win32`  | 
| Windows 64-Bit   | `win64` |
| Mac OS | `macos` |
| Linux  | `linux` |
| FreeBSD  | `freebsd` |
| AmigaOS  | `amiga` |
| Android  | `android` |
| OpenBSD, NetBSD, DragonFly  | `bsd` |
| Cygwin  | `cygwin` |
| Minix  | `minix` |
| Solaris  | `solaris` |
| Symbian | `symbian` |
| z/VM | `zvm` |

For other OSs, `os_name` will return `unknown`.

## `system(command:string) : int`
Executes a command and returns command's exit code.

Example :
```typescript
system("gcc main.c")
```

## `compiler_name() : string`
Returns Hascal C\C++ compiler name.

| Compiler      | `compiler_name()` output  | 
| :------------- | :----------: | 
| GCC\G++  | `gcc`  | 
| Clang(LLVM)  | `clang`  | 
| Microsoft Visual C++  | `msvc`  | 
| Digital Mars C\C++ | `dmc`  | 
| Intel C\C++ | `icc`  | 

For other compilers, `compiler_name` will return `unknown`.

## `arch() : string`
Returns CPU architecture.

| Architecture      | `arch()` output  | 
| :------------- | :----------: | 
| x86  | `intel32`  | 
| x86_64  | `amd64`  | 
| Arm  | `arm`  | 
| Intel Itanium 64-Bit | `ia64`  | 
| Mips  | `mips`  | 
| PowerPC  | `powerpc`  | 


## `is_x86() : bool`
Returns true if CPU architecture is x86.

## `is_x64() : bool`
Returns true if CPU architecture is x86_64.