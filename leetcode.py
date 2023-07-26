from pprint import pp
import re
import requests
import json
import random

# url to JS file of neetcode script that populates data

class Leetcode:

    def __init__(self):
        self.url = "https://neetcode.io/main.e9d3b0a379eb0fd4.js"
        self.rand = random.randint(0, 74)
        self.data_json = self.parse_data(self.url)

    def parse_data(self, url) -> json:

        r = requests.get(url, timeout=3)
        js_code = r.text

        # parses the JS file to get the array lists
        matches = re.findall(r'C=(\[.*?\])', js_code, re.DOTALL)
        for match in matches:
            # print(match)
            if match == '[]' or not match:
                continue
            if match == "['*']" or match == '["*"]':
                continue

            # converts the string into JSON
            match = match.replace('!0', 'true').replace('!1', 'false')

            # More specific matching for key-value pairs
            match = re.sub(r'(?<={|,)\s*([\'"]?\w+[\'"]?)\s*:', r'"\1":', match)

            json_objects = json.loads(match)
            json_objects = [obj for obj in json_objects if obj.get('blind75') is True]

            return json_objects
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
        
 
if __name__ == '__main__':
    l = Leetcode()
    print(l.get_leetcode_url(), l.get_solution_url(), l.get_youtube_url())