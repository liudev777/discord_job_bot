import requests
from bs4 import BeautifulSoup

proxy = '129.153.157.63:3128'

response1 = requests.get('https://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=3)
print(response1.json())
try:
    response2 = requests.get('https://techcrunch.com/2023/07/21/foreign-visitors-to-china-can-finally-go-cashless-like-locals/', proxies={'http': proxy, 'https': proxy}, timeout=3)
    print(response2.status_code)
    print(response2.text)
    soup = BeautifulSoup(response2.text, "html.parser")
    title = soup.find("h1", attrs={"class": "article__title"})
    print(title.text)
except TimeoutError:
    print("timed out\n")