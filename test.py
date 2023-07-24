import re
import requests
import json

# This is your JavaScript code as a string
url = "https://neetcode.io/main.e9d3b0a379eb0fd4.js"

r = requests.get(url, timeout=3)
js_code = r.text
# print(js_code)
# Find the array in the JavaScript code
matches = re.findall(r'C=\[(.*?)\]', js_code, re.DOTALL)
for match in matches:
    if not match:
        continue
    if match == '*':
        continue
    with open('match.txt', 'w') as f:
        f.write(match + "\n")