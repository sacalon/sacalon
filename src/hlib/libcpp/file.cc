std::string read_file(std::string path){
	std::string tmp;
	std::string res;
	std::ifstream file;
	file.open(path.c_str());
	if(!file.good()){
		throw std::runtime_error(std::string("File not found or access is denied"));
	}
	while(getline(file,tmp)){
		res += tmp + "\n";
	}
	
	return res;
}

bool write_file(std::string path,std::string text){
	try {
		std::ofstream file;
		file.open(path.c_str());
		file << text;
		file.close();
		return true;
	}catch (int x){
		throw std::runtime_error(std::string("Cannot write the file"));
	}
	return false;
}
