import std.random;

int RandomNumber(int min,int max){
	auto rnd = Random(unpredictableSeed);
	return uniform(min,max, rnd);
}