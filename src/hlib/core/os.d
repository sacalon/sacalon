string os_name(){
	OS myOS;
	switch(int(myOS)){
        case 1 :
            return "win32";
        case 2 :
            return "win64";
        case 3 :
            return "linux";
        case 4 :
            return "osx";
        case 5 :
            return "freebsd";
        case 6 :
            return "netbsd";
        case 7 :
            return "dragonFlyBSD";
        case 8 :
            return "solaris";
        case 9 :
            return "android";
        case 10 :
            return "otherPosix";
        default : 
            return "unknown";
    }
    return "";
}


void ExcuteCommand(string com){
	auto comm = com.split(" ");

	if(com == null){
		writeln("Runtime Error : command cannot empty");
		goto exit;
	}
	
	if(comm[0] == null){
		writeln("Runtime Error : command cannot empty");
		goto exit;
	}

	try {
		auto prc = execute(comm);
		writeln(prc.output);
	}catch(Exception e){
		writeln("Runtime error : cannot excute command");
	}

	exit:
		auto tmp = 0;
		tmp++;
}


void ShellCommand(string com){
	try {
		auto prc = executeShell(com);
		if (prc.status != 0){
			writeln("Runtime Error : cannot excute command");
		}else {
			writeln(prc.output);
		}
	}catch(Exception e) {
		writeln("Runtime Error : cannot excute command");
	}
}
