
int to_int(string s){
	return std::stoi(s);
}

int __hascal__to_int(float s){
	return (int)s;
}

int __hascal__to_int(bool s){
	return (int)s;
}

int __hascal__to_int(int s){
	return s;
}

int __hascal__to_int(char s){
	return (int)s-48; // ASCII chars start with 48
}

string __hascal__to_string(int s){
	string res = std::to_string(s);
	return res;
}

string __hascal__to_string(char s){
	string res = { s };
	return res;
}

string __hascal__to_string(char* s){
	string res = s;
	return res;
}

string __hascal__to_string(string s){
	return s;
}

string __hascal__to_string(float s){
	return std::to_string(s);
}

string __hascal__to_string(bool s){
	if(s == true)
		return "true";
	return "false";
}

float __hascal__to_float(int s){
	return (float)s;
}

float __hascal__to_float(string s){
	return std::stof(s);
}

float __hascal__to_float(float s){
	return s;
}

float __hascal__to_float(bool s){
	if(s == true)
		return 1.0;
	return 0.0;
}

char __hascal__to_char(int s){
	return (char)(s+48);
}

char __hascal__to_char(char c){
	return c;
}

char* __hascal__c_str(std::string s){
	char* res = const_cast<char*>(s.c_str());
	return res;
}