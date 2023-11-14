static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
    ((string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

string __sacalon__get(string url){
    CURL *curl;
    CURLcode res;
    string readBuffer;

    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        res = curl_easy_perform(curl);
        curl_easy_cleanup(curl);

        if(res != CURLE_OK)
            fprintf(stderr, "curl_easy_perform() failed: %s\n",
                curl_easy_strerror(res));
            
        return readBuffer + "\n";
    }
    return "";
}

string __sacalon__post(string url,string post_data){
    CURL *curl;
    CURLcode res;
    string readBuffer;

    curl_global_init(CURL_GLOBAL_ALL);
    
    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_data.c_str());
        res = curl_easy_perform(curl);

        if(res != CURLE_OK)
        fprintf(stderr, "curl_easy_perform() failed: %s\n",
                curl_easy_strerror(res));
    
        curl_easy_cleanup(curl);
    }
    curl_global_cleanup();
    return readBuffer + "\n";
}

bool __sacalon__download(string url,string path){
    auto res = __sacalon__get(url);
    return __sacalon__write_file(path,res);
}

bool __sacalon__upload(string url,string path){
    CURL *curl;
    CURLcode res;
    struct stat file_info;
    curl_off_t speed_upload, total_time;
    FILE *fd;

    fd = fopen(path.c_str(), "rb"); /* open file to upload */
    if(!fd)
        return false; /* cannot continue */

    /* to get the file size */
    if(fstat(fileno(fd), &file_info) != 0)
        return false; /* cannot continue */

    curl = curl_easy_init();
    if(curl) {
        /* upload to this place */
        curl_easy_setopt(curl, CURLOPT_URL,url.c_str());
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
        curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
        /* tell it to "upload" to the URL */
        curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);

        string osname = __sacalon__os_name();
        if(osname == "win32" || osname == "win64")
            curl_easy_setopt(curl, CURLOPT_READFUNCTION, fd);
        curl_easy_setopt(curl, CURLOPT_READDATA, fd);

        /* enable verbose for easier tracing */
        curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);

        res = curl_easy_perform(curl);
        /* Check for errors */
        if(res != CURLE_OK) {
        fprintf(stderr, "curl_easy_perform() failed: %s\n",
                curl_easy_strerror(res));
        }
        /* always cleanup */
        curl_easy_cleanup(curl);
    } else {
        return false;
    }
    return true;
}