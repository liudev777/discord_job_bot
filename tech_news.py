import requests
from bs4 import BeautifulSoup

# proxy = '129.153.157.63:3128'

response1 = requests.get('https://httpbin.org/ip')
print(response1.json())
try:
    url = 'https://hackernoon.com/tagged/hackernoon-top-story'
    r = requests.get(url)
    print(r.status_code)
    with open("out.html", "w") as f:
        print(r.text, file=f)
except TimeoutError:
    print("timed out\n")