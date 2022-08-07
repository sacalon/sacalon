int __hascal__randint(int max, int min)
{
    srand(time(NULL));
    return rand() % max + min;
}

float __hascal__uniform(float max, float min)
{
    srand(time(NULL));
    return (float)rand() / (float)RAND_MAX * (max - min) + min;
}

double __hascal__uniform(double max, double min)
{
    srand(time(NULL));
    return (double)rand() / (double)RAND_MAX * (max - min) + min;
}