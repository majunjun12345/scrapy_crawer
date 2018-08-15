import hashlib

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    return hashlib.md5(url).hexdigest()


if __name__ == "__main__":
    url = "https://www.baidu.com"
    print(get_md5(url.encode('utf-8')))