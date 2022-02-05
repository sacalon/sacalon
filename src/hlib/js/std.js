function error(msg){
    throw new Error(msg);
}

function panic(msg){
    error(msg)
}

function ReadStr(){
    return prompt("");
}

function ReadStr(msg){
    return prompt(msg);
}

function ReadInt(){
    return parseInt(ReadStr());
}

function ReadInt(msg){
    return parseInt(ReadStr(msg));
}

function ReadFloat(){
    return parseFloat(ReadStr());
}

function ReadFloat(msg){
    return parseFloat(ReadStr(msg));
}

function ReadChar(){
    return ReadStr().charAt(0);
}

function ReadChar(msg){
    return ReadStr(msg).charAt(0);
}

function ReadBool(){
    return ReadStr().toLowerCase() == "true";
}

function ReadBool(msg){
    return ReadStr(msg).toLowerCase() == "true";
}

function len(obj){
    return obj.length;
}

function append(obj, item){
    obj.push(item);
}

function split(str, sep){
    return str.split(sep);
}

function format(fmtstr, ...args){
    var res = "";
    var points = fmtstr.split("{}");
    for(var i = 0; i < points.length; i++){
        res += points[i];
        if(i < args.length)
            res += args[i];
    }
    return res;
}