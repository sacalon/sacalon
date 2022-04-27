
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

char to_char(int s){
	return (char)(s+48);
}

char to_char(char c){
	return c;
}

char* c_str(std::string s){
	char* res = const_cast<char*>(s.c_str());
	return res;
}