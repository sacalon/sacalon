int __sacalon__randint(int min, int max)
{
    srand(time(NULL));
    return rand() % max + min;
}

float __sacalon__uniform(float min, float max)
{
    srand(time(NULL));
    float scale = rand() / (float) RAND_MAX; /* [0, 1.0] */
    return min + scale * ( max - min );      /* [min, max] */
}

double __sacalon__uniform(double min, double max)
{
    srand(time(NULL));
    double scale = rand() / (double) RAND_MAX; /* [0, 1.0] */
    return min + scale * ( max - min );      /* [min, max] */
}