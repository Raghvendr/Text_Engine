from urllib.parse import urlencode, urlparse, parse_qs

from lxml.html import fromstring
from requests import get

raw = get("https://www.google.com/search?q=StackOverflow").text
page = fromstring(raw)

for result in pg.cssselect(".r a"):
    url = result.get("href")
    if url.startswith("/url?"):
        url = parse_qs(urlparse(url).query)['q']
    print(url[0])
