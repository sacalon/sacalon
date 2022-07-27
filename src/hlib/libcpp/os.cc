string __hascal__os_name()
{
    #ifdef _WIN32
    return "win32";
    #elif _WIN64
    return "win64";
    #elif __APPLE__ || __MACH__ || macintosh || Macintosh
    return "macos";
    #elif __linux__
    return "linux";
    #elif __FreeBSD__
    return "freebsd";
    #elif __unix || __unix__
    return "unix";
    #elif __ANDROID__
    return "android";
    #elif AMIGA
    return "amiga";
    #elif __FreeBSD__ || __OpenBSD__ || __NetBSD__ || __DragonFly__
    return "bsd";
    #elif __CYGWIN__
    return "cygwin";
    #elif __minix
    return "minix";
    #elif __MSDOS__
    return "msdos";
    #elif __sun
    return "solaris";
    #elif __SYMBIAN32__
    return "symbian";
    #elif __MVS__
    return "zvm";
    #else
    return "unknown";
    #endif
}

int __hascal__system(string cmd)
{
    return system(cmd.c_str());
}

bool __hascal__is_x86(){
    if(sizeof(void*) == 4)
        return true;
    else
        return false;
}

bool __hascal__is_64(){
    return !__hascal__is_x86();
}

string __hascal__compiler_name(){
    #ifdef __clang__
    return "clang";
    #elif __GNUC__
    return "gcc";
    #elif _MSC_VER
    return "msvc";
    #elif __BORLANDC__
    return "bcc";
    #elif __DMC__
    return "dmc";
    #elif __INTEL_COMPILER
    return "icc";
    #else
    return "unknown";
    #endif
}


// refernce: https://sourceforge.net/p/predef/wiki/Architectures/
string __hascal__arch()
{
    string comname = __hascal__compiler_name();

    if(comname == "msvc"){
        #ifdef _M_AMD64
        return "AMD64";
        #elif _M_IX86
        return "intel32";
        #elif _M_IA64
        return "itanium";
        #elif _M_PPC
        return "powerpc";
        #else
        return "unknown";
        #endif
    }else if(comname == "gcc"){
        #ifdef __amd64__ || __amd64
        return "AMD64";
        #elif __arm__
        return "arm";
        #elif __i386__ || __i486__ || __i586__ || __i686__
        return "intel32";
        #elif __ia64__
        return "ia64";
        #elif __mips__
        return "mips";
        #elif __powerpc__ || __powerpc64__
        return "powerpc";
        #else
        return "unknown";
        #endif
    }else if(comname == "icc"){
        #ifdef __itanium__
        return "itanium";
        // TODO : Add support for more compilers
        #endif
    }
    return "unknown";
}