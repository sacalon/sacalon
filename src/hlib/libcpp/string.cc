bool is_alpha(char c){
    return std::is_alpha(c);
}

bool is_alphanum(char c){
    return std::is_alpha(c) || std::is_digit(c);
}

bool is_space(char c){
    return std::isspace(c);
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