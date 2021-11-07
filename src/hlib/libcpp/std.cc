typedef string string;

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

