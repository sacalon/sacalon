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