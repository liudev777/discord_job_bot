from pprint import pp
import re
import requests
import json
import random
from bs4 import BeautifulSoup

""" 
url to JS file of neetcode script that populates data 
"""

class Neetcode:

    def __init__(self):
        self.url = self.find_script_url()
        self.rand = random.randint(0, 74)
        self.data_json = self.parse_data(self.url)

    def find_script_url(self, page_url="https://neetcode.io/") -> str:
        r = requests.get(page_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        scripts = soup.find_all('script')

        for script in scripts:
            if not script.get('src'):
                continue
            src = script['src']
            if not src.startswith('main.'):
                continue
            return f'https://neetcode.io/{src}'
        return None

    def parse_data(self, url) -> json:
        r = requests.get(url, timeout=3)
        js_code = r.text

        # parses the JS file to get the array lists.
        matches = re.findall(r'\[\{neetcode150:.*?,blind75:.*?\}.*?\]', js_code, re.DOTALL)
        for match in matches:
            # converts the string into JSON
            match = match.replace('!0', 'true').replace('!1', 'false')

            # More specific matching for key-value pairs
            match = re.sub(r'(?<={|,)\s*([\'"]?\w+[\'"]?)\s*:', r'"\1":', match)

            try:
                json_objects = json.loads(match)
                json_objects = [obj for obj in json_objects if obj.get('blind75') is True]
                return json_objects
            except json.JSONDecodeError:
                print(f"Failed to parse JSON: {match}")
                continue
        return None


    def get_youtube_url(self) -> str:
        endpoint = self.data_json[self.rand].get("video")
        return f'https://www.youtube.com/watch?v={endpoint}'
    
    def get_solution_url(self) -> str:
        endpoint = self.data_json[self.rand].get("code")
        return f'https://github.com/neetcode-gh/leetcode/blob/main/python/{endpoint}.py'
    
    def get_leetcode_url(self) -> str:
        endpoint = self.data_json[self.rand].get("link")
        return f'https://leetcode.com/problems/{endpoint}'
        
    def get_name(self) -> str:
        endpoint = self.data_json[self.rand].get("problem")
        return str(endpoint)
    
    def get_solution_raw(self) -> str:
        endpoint = self.data_json[self.rand].get("code")
        r = requests.get(f"https://raw.githubusercontent.com/neetcode-gh/leetcode/main/python/{endpoint}.py")
        if r.status_code != 200:
            print(r.status_code)
            return "No Solution"
        return r.text
 
 
if __name__ == '__main__':
    l = Neetcode()
    print(l.get_leetcode_url(), l.get_solution_url(), l.get_youtube_url())