int RandInt(int max){
    srand((unsigned) time(0));
    return (rand() % max) + 1;
}