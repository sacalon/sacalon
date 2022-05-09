float mean(std::vector<int> const& v) {
    int n = 0;
    float mean = 0.0;
    for (auto x : v) {
        float delta = x - mean;
        mean += delta/++n;
    }
    return mean;
}

float mean(std::vector<float> const& v) {
    int n = 0;
    float mean = 0.0;
    for (auto x : v) {
        float delta = x - mean;
        mean += delta/++n;
    }
    return mean;
}