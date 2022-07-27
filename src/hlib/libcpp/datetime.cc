int __hascal__get_year(){
	std::time_t t = std::time(0);
	std::tm* now = std::localtime(&t);
	return (int) (now->tm_year + 1900);
}

int __hascal__get_month(){
	std::time_t t = std::time(0);
	std::tm* now = std::localtime(&t);
	return (int) (now->tm_mon + 1);
}

int __hascal__get_day(){
	std::time_t t = std::time(0);
	std::tm* now = std::localtime(&t);
	return (int) now->tm_mday;
}

int __hascal__get_hour(){
	std::time_t t = std::time(0);
	std::tm* now = std::localtime(&t);
	return (int) now->tm_hour;
}

int __hascal__get_minute(){
	std::time_t t = std::time(0);
	std::tm* now = std::localtime(&t);
	return (int) now->tm_min;
}

int __hascal__get_second(){
	std::time_t t = std::time(0);
	std::tm* now = std::localtime(&t);
	return (int) now->tm_sec;
}