float __hascal__mean(std::vector<int> const& v) {
    float mean = 0.0;
    for (auto x : v) {
        mean += x;
    }
    mean = mean / v.size();
    return mean;
}

float __hascal__mean(std::vector<float> const& v) {
    float mean = 0.0;
    for (auto x : v) {
        mean += x;
    }
    mean = mean / v.size();
    return mean;
}

double __hascal__pow(double a,double b){
    return pow(a,b);
}

float __hascal__round(float arg){
    return std::round(arg);
}

double __hascal__round(double arg){
    return std::round(arg);
}