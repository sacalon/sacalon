int __hascal__random_int(int max, int min)
{
    srand(time(NULL));
    return rand() % max + min;
}