string libc_name(){
    #ifdef __GNU_LIBRARY__ || __GLIBC__
    return "glibc";
    #elif __KLIBC__
    return "klibc";
    #elif __UCLIBC__
    return "uclibc";
    #elif __LIBREL__ || __RELIX__
    return "libre";
    #elif __GLIBCPP__ || __GLIBCXX__
    return "libcpp";
    #elif _LIBCPP_VERSION
    return "libcpp";
    #elif _MFC_VER
    return "mfc";
    #else 
    return "unknown";
    #endif
    return "unknown";
}