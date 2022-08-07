std::string __hascal__read_file(std::string path){
	std::string tmp;
	std::string res;
	std::ifstream file;
	file.open(path.c_str());
	if(!file.good()){
		throw HascalException(std::string("File not found or access is denied"));
	}
	while(getline(file,tmp)){
		res += tmp + "\n";
	}
	
	return res;
}

bool __hascal__write_file(std::string path,std::string text){
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