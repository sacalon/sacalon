#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <cstdarg>
#include <cstring>
#include <type_traits>
#include <typeinfo>
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

// exit()


#include <cctype>





#include <cctype>


bool is_alpha(char c){
    return std::isalpha(c);
}

bool is_alphanum(char c){
    return std::isalpha(c) || std::isdigit(c);
}

bool is_space(char c){
    return std::isspace(c);
}

bool is_number(char c){
    return std::isdigit(c);
}

string to_lower(string str){
    string temp;
    for (char c : str)
    {
        temp += std::tolower(c);
    }
    return temp;
}

string to_upper(string str){
    string temp;
    for (char c : str)
    {
        temp += std::toupper(c);
    }
    return temp;
}



struct token{
string kind ;
string value ;

};
std::vector<token> tokenizer( string input) {
input = input + std::string("\n");auto current = 0;
std::vector<token> tokens;
while(current < len(input)){
auto ch = to_char(input[current]);
if(ch == '('){
append(tokens, {std::string("paren"),std::string("(")});
current = current + 1;continue;

}
if(ch == ')'){
append(tokens, {std::string("paren"),std::string(")")});
current = current + 1;continue;

}
if(ch == ' '){
current = current + 1;continue;

}
if(is_number(ch)){
auto value = std::string("");
while(is_number(ch) == true){
value = value + to_string(ch);current = current + 1;ch = to_char(input[current]);
}
append(tokens, {std::string("number"),value});
continue;

}
if(is_number(ch) == true){
auto value = std::string("");
while(is_number(ch) == true){
value = value + to_string(ch);current = current + 1;ch = to_char(input[current]);
}
append(tokens, {std::string("name"),value});
continue;

}
break;

}
return tokens;

}
struct node_t{

};
struct node{
string kind ;
string value ;
string name ;
node* callee ;
node* expression ;
std::vector<node> body;
std::vector<node> params;
node* arguments ;
node* context ;

};
struct ast : node{

};
int pc ;
std::vector<token> pt;
node walk() {
token tok = pt[pc];
if(tok.kind == std::string("number")){
pc = pc + 1;return node{std::string("NumberLiteral"), tok.value};

}
if(tok.kind == std::string("paren") && tok.value == std::string("(")){
pc = pc + 1;tok = pt[pc];node n = node{std::string("CallExpression"), tok.value};
pc = pc + 1;tok = pt[pc];while(tok.kind != std::string("paren") && (tok.kind == std::string("paren") && tok.value != std::string(")"))){
append(n.params, walk());
tok = pt[pc];
}
pc = pc + 1;return n;

}
error(std::string("Unexpected token"));
return node{};

}
ast parser( std::vector<token> tokens) {
pc = 0;pt = tokens;auto result_ast = ast{std::string("Program")};
while(pc < len(pt)){
append(result_ast.body, walk());

}
return result_ast;

}
int main(int argc,char** args) {
std::vector<std::string> argv;for(int i=0;i<argc;i++){argv.push_back(args[i]);}
return 0;

}

