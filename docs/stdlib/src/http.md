# `http`
HTTP-client library.

> **NOTE** : If you want to use `http` library, your C++ backend compiler should have [`libcurl`](https://curl.se/libcurl/) and [its dsependencies](https://curl.se/docs/libs.html).

## `get(url:string) : string`
get content from given url.

## `post(url:string,data:string):string`
post content to given url.
- `url` : url to post `data`
- `data` : post data

Example :
```typescript
post("https://example.com/post.php","name=john&family=doe")
```

## `download(url:string,path:string):bool`
download and save a url to storage.
- `url` : your file url to download
- `path` : path to save downloaded file

## `upload(url:string,path:string):bool`
upload a file to a url.
- `url` : your url to upload file
- `path` : path to your file to upload


[See example for http library](https://github.com/sacalon-lang/sacalon/blob/main/examples/net.sa)
