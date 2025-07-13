std::string __sacalon__read_file(std::string path){
	std::string tmp;
	std::string res;
	std::ifstream file;
	file.open(path.c_str());
	if(!file.good()){
		throw SacalonException(std::string("File not found or access is denied"));
	}
	while(getline(file,tmp)){
		res += tmp + "\n";
	}
	
	return res;
}

bool __sacalon__write_file(std::string path,std::string text){
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

std::string __sacalon__fread_line(FILE* file) {
    char buffer[1024];
    if (fgets(buffer, sizeof(buffer), file)) {
        // حذف کاراکتر خط جدید (اختیاری)
        buffer[strcspn(buffer, "\n")] = '\0';
        return std::string(buffer);
    }
    return ""; // یا throw exception
}