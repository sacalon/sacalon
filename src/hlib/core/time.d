int GetYear(){

	try {
		SysTime today = Clock.currTime();
		return today.year;
	}catch(Exception e){
		writeln("Runtime Error : GetYear() function crashed");
	}
	return 0 ;
}

int GetMonth(){
	try {
		SysTime today = Clock.currTime();
		return today.month;
	}catch(Exception e){
		writeln("Runtime Error : GetMonth() function crashed");
	}
	return 0 ;
}

int GetDay(){
	try {
		SysTime today = Clock.currTime();
		return today.day;
	}catch(Exception e){
		writeln("Runtime Error : GetDay() function crashed");
	}
	return 0 ;
}

int GetHour(){
	try {
		SysTime today = Clock.currTime();
		return today.hour;
	}catch(Exception e){
		writeln("Runtime Error : GetHour() function crashed");
	}
	return 0 ;
}

int GetMinute(){
	try {
		SysTime today = Clock.currTime();
		return today.minute;
	}catch(Exception e){
		writeln("Runtime Error : GetMinute() function crashed");
	}
	return 0 ;
}

int GetSecond(){
	try {
		SysTime today = Clock.currTime();
		return today.second;
	}catch(Exception e){
		writeln("Runtime Error : GetSecond() function crashed");
	}
	return 0 ;
}
