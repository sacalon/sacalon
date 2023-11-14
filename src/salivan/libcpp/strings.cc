bool __sacalon__is_alpha(char c){
    return std::isalpha(c);
}

bool __sacalon__is_alphanum(char c){
    return std::isalpha(c) || std::isdigit(c);
}

bool __sacalon__is_space(char c){
    return std::isspace(c);
}

bool __sacalon__is_number(char c){
    return std::isdigit(c);
}

string __sacalon__to_lower(string str){
    string temp;
    for (char c : str)
    {
        temp += std::tolower(c);
    }
    return temp;
}

string __sacalon__to_upper(string str){
    string temp;
    for (char c : str)
    {
        temp += std::toupper(c);
    }
    return temp;
}