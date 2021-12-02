typedef std::string string;

void error(string err_msg){
	std::cerr << err_msg << std::endl ;
}

int to_int(string s){
	return std::stoi(s);
}

int to_int(float s){
	return (int)s;
}

int to_int(bool s){
	return (int)s;
}

int to_int(int s){
	return s;
}

int to_int(char s){
	return (int)s-48; // ASCII chars starts with 48
}

string to_string(int s){
	string res = std::to_string(s);
	return res;
}

string to_string(char s){
	string res = { s };
	return res;
}

string to_string(char* s){
	string res = s;
	return res;
}

string to_string(string s){
	return s;
}

string to_string(float s){
	return std::to_string(s);
}

string to_string(bool s){
	if(s == true)
		return "true";
	return "false";
}

float to_float(int s){
	return (float)s;
}

float to_float(string s){
	return std::stof(s);
}

float to_float(float s){
	return s;
}

float to_float(bool s){
	if(s == true)
		return 1.0;
	return 0.0;
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

template<typename Test, template<typename...> class Ref>
struct is_specialization : std::false_type {};

template<template<typename...> class Ref, typename... Args>
struct is_specialization<Ref<Args...>, Ref>: std::true_type {};

int len(string s){
	return s.length();
}

bool regex(string regex_string,string str){
    if(std::regex_match(regex_string, std::regex(str) ))
        return true;
    return false;
}

// this function is used to get length of a vector
template <typename T>
int len(std::vector<T> v){
	return v.size();
}

// this function is used to get length of a string
template <typename T>
int len(T s){
	return s.length();
}

// exit()