#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <cstdarg>
#include <cstring>
#include <type_traits>
#include <typeinfo>
// #include <unordered_map>
#include <string_view>
#include <exception>
#include <functional>

typedef std::string string;

// should support all compilers(todo)
// #if __GNUC__ || __clang__
// typedef __int128 int128;
// #else
// typedef __int128_t int128;
// #endif

typedef long long int64;
typedef unsigned long long uint64;

typedef unsigned int uint;
typedef unsigned long long uint64;

typedef short int16;
typedef unsigned short uint16;

typedef unsigned char uint8;
typedef char int8;

// #define dict std::unordered_map

void error(string err_msg){
	std::cerr << err_msg << std::endl ;
}

void panic(string err_msg){
	error(err_msg);
	exit(1);
}


string ReadStr(){
	string res;
	std::cin >> res;
	return res;
}

string ReadStr(string p){
	std::cout << p;
	string res;
	std::cin >> res;
	return res;
}

char ReadChar(){
	char res;
	std::cin >> res;
	return res;
}

char ReadChar(string p){
	std::cout << p;
	char res;
	std::cin >> res;
	return res;
}

bool ReadBool(){
	string tmp = ReadStr();
	if(tmp == "0" || tmp == "true")
		return true;
	return false;
}

bool ReadBool(string p){
	string tmp = ReadStr(p);
	if(tmp == "0" || tmp == "true")
		return true;
	return false;
}

int ReadInt(){
	int res;
	std::cin >> res;
	return res;
}

int ReadInt(string p){
	std::cout << p;
	int res;
	std::cin >> res;
	return res;
}

float ReadFloat(){
	float res;
	std::cin >> res;
	return res;
}

float ReadFloat(string p){
	std::cout << p;
	float res;
	std::cin >> res;
	return res;
}



template<typename Test, template<typename...> class Ref>
struct is_specialization : std::false_type {};

template<template<typename...> class Ref, typename... Args>
struct is_specialization<Ref<Args...>, Ref>: std::true_type {};

// this function is used to get length of a vector
template <typename T>
int len(std::vector<T> v){
	return v.size();
}

// this function is used to get length of a string
int len(string s){
	return s.length();
}

// this function is used to append a value to a vector
template <typename T>
void append(std::vector<T>& v, T val){
	v.push_back(val);
}

string input(){
	return ReadStr();
}
string input(string text){
	return ReadStr(text);
}

std::vector<std::string> split(std::string str,std::string sep){
    char* cstr=const_cast<char*>(str.c_str());
    char* current;
    std::vector<std::string> arr;
    current=strtok(cstr,sep.c_str());
    while(current!=NULL){
        arr.push_back(current);
        current=strtok(NULL,sep.c_str());
    }
    return arr;
}

// format function -> e.g : format("Hi, {}",name)
template <typename T, typename ... ARGS>
string format(T text,ARGS... args){
	string res;

	std::vector<string> fmt_list = { args... };
  	std::vector<string> points = split(text,"{}");

  	int fmt_size = fmt_list.size();
  	int points_size = points.size();

  	for(int i,j=0;i<=points_size-1 && j<=fmt_size;j++,i++){
		res += points[i] + fmt_list[j];
  	} 
	return res;
}

template <typename T>
T* mem_new(T val){
	T* res = new T(val);
	return res;
}
template <typename T>
T* mem_realloc(T* ptr, T val){
	delete ptr;
	T* res = new T(val);
	return res;
}
template <typename T>
void mem_delete(T* ptr){
	delete ptr;
}
template <typename T>
std::vector<T>* mem_new(){
	auto res = new std::vector<T>();
	return res;
}
template <typename T>
std::vector<T>* mem_renew(std::vector<T>* ptr,std::vector<T> val){
	delete ptr;
	auto res = new std::vector<T>(val);
	return res;
}
template <typename T>
void mem_delete(std::vector<T>* ptr){
	delete ptr;
}


template <typename T>
constexpr auto __hascal___type_name() {
  	std::string_view name, prefix, suffix;
#ifdef __clang__
  	name = __PRETTY_FUNCTION__;
  	prefix = "auto type_name() [T = ";
  	suffix = "]";
#elif defined(__GNUC__)
  	name = __PRETTY_FUNCTION__;
  	prefix = "constexpr auto type_name() [with T = [with T =  ";
  	suffix = "]";
#elif defined(_MSC_VER)
  	name = __FUNCSIG__;
  	prefix = "auto __cdecl type_name<";
  	suffix = ">(void)";
#endif
  	name.remove_prefix(prefix.size());
  	name.remove_suffix(suffix.size());
  	return name;
}

template <typename T>
std::string typeof(T val) {
	std::string res(__hascal___type_name<decltype(val)>());
	if (res == "std::__cxx11::basic_string<char>")
		return "string";
	
	return res;
}

template <typename T>
std::ostream& operator<< (std::ostream& out, const std::vector<T>& v) {
	out << "[";
  for (auto it = v.begin(); it != v.end(); ++it) {
	if (typeof(*it) == "string"){
		out << "\"" << *it << "\"";
	} else if(typeof(*it) == "char"){
		out << "'" << *it << "'";		
	}else {
		out << *it;
	}

	if (it != v.end() - 1) {
	  out << ", ";
	}
  }
  out << "]";
  return out;
}

struct HascalException : public std::exception
{
	std::string msg;
	HascalException(std::string msg){
		this->msg = msg;
	}
	const char * what () const throw ()
    {
    	return this->msg.c_str();
    }
};
// exit()




#include <curl/curl.h>
#include <string>
#include <sys/stat.h>
#include <fcntl.h>








#include <curl/curl.h>
#include <string>
#include <sys/stat.h>
#include <fcntl.h>







#include <fstream>
std::string read_file(std::string path){
	std::string tmp;
	std::string res;
	std::ifstream file;
	file.open(path.c_str());
	if(!file.good()){
		throw HascalException(std::string("File not found or access is denied"));
	}
	while(getline(file,tmp)){
		res += tmp + "\n";
	}
	
	return res;
}

bool write_file(std::string path,std::string text){
	try {
		std::ofstream file;
		file.open(path.c_str());
		file << text;
		file.close();
		return true;
	}catch (int x){
		return false;
	}
	return false;
}




static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
    ((string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

string get(string url){
    CURL *curl;
    CURLcode res;
    string readBuffer;

    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);

        if(res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n",
                curl_easy_strerror(res));
            
        return readBuffer + "\n";
    }
    return "";
}

string post(string url,string post_data){
    CURL *curl;
    CURLcode res;
    string readBuffer;

    curl_global_init(CURL_GLOBAL_ALL);
    
    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_data.c_str());
        res = curl_easy_perform(curl);

        if(res != CURLE_OK)
        fprintf(stderr, "curl_easy_perform() failed: %s\n",
                curl_easy_strerror(res));
    
        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();
    return readBuffer + "\n";
}

bool download(string url,string path){
    auto res = get(url);
    return write_file(path,res);
}

bool upload(string url,string path){
    CURL *curl;
    CURLcode res;
    struct stat file_info;
    curl_off_t speed_upload, total_time;
    FILE *fd;

    fd = fopen(path.c_str(), "rb"); /* open file to upload */
    if(!fd)
        return false; /* cannot continue */

    /* to get the file size */
    if(fstat(fileno(fd), &file_info) != 0)
        return false; /* cannot continue */

    curl = curl_easy_init();
    if(curl) {
        /* upload to this place */
        curl_easy_setopt(curl, CURLOPT_URL,url.c_str());
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
        /* tell it to "upload" to the URL */
        curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);

        string osname = os_name()
        if(osname == "win32" || osname == "win64")
            curl_easy_setopt(curl, CURLOPT_READFUNCTION, fd);
        curl_easy_setopt(curl, CURLOPT_READDATA, fd);

        /* enable verbose for easier tracing */
        curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);

        res = curl_easy_perform(curl);
        /* Check for errors */
        if(res != CURLE_OK) {
        fprintf(stderr, "curl_easy_perform() failed: %s\n",
                curl_easy_strerror(res));
        }
        /* always cleanup */
        curl_easy_cleanup(curl);
    } else {
        return false;
    }
    return true;
}



 int main() {
std::cout << get(std::string("http://google.com")) << std::endl;
return 0;

}

