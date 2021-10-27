void RemoveFile(string s){
	try {
		std.file.remove(s);
	}catch(Exception e){
		writeln("Runtime Error : cannot remove '",s,"' file");
	}
}

string ReadFromFile(File file){
	try{
		string tmp;
		auto f = File(file.name,"r");
		f.readf!"%s"(tmp);
		return tmp;
	}catch(Exception e){
		writeln("Runtime Error : cannot read '",file.name,"' file.");
	}
	return "";
}

void WriteToFile(File myfile,string s){
	try {
		myfile.write(s);
	}catch(Exception e){
		writeln("Runtime Error : cannot write to '",myfile.name,"'.");
	}
}

void CloseFile(File myfile){
	try {
		myfile.close;
	}catch(Exception e){
		writeln("Runtime Error : cannot close '",myfile.name,"' file.");
	}
}

string[] listdir(string pathname)
{
    import std.algorithm;
    import std.array;
    import std.file;
    import std.path;

    return std.file.dirEntries(pathname, SpanMode.shallow)
        .filter!(a => a.isFile)
        .map!(a => std.path.baseName(a.name))
        .array;
}

