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

// exit()