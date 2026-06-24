import httpx
from urllib.parse import urlparse

def is_cross_origin(url1: str, url2: str) -> bool:
    u1 = urlparse(url1)
    u2 = urlparse(url2)
    if not u2.netloc:
        return False
    return (u1.scheme, u1.netloc) != (u2.scheme, u2.netloc)

client = httpx.Client()
url = httpx.URL("http://example.com/api")
print(type(url))
print(str(url))
print(is_cross_origin(str(url), "http://example.com/other"))
print(is_cross_origin(str(url), "https://example.com/other"))
print(is_cross_origin(str(url), "/other"))
print(is_cross_origin(str(url), "http://other.com/other"))
