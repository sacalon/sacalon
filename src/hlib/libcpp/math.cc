float mean(std::vector<int> const& v) {
    float mean = 0.0;
    for (auto x : v) {
        mean += x;
        n++;
    }
    mean = mean / v.size();
    return mean;
}

float mean(std::vector<float> const& v) {
    float mean = 0.0;
    for (auto x : v) {
        mean += x;
        n++;
    }
    mean = mean / v.size();
    return mean;
}