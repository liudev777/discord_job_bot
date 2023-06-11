import requests
import os
import dotenv

dotenv.load_dotenv()

"""
jsearch api requests
"""

class Jsearch:
    def __init__(self, query):
        self.url = "https://jsearch.p.rapidapi.com/search"
        self.querystring = {"query": f"{query}","page":"1","num_pages":"1"}

        self.headers = {
            "X-RapidAPI-Key": os.environ['RAPID_API_KEY'],
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

        self.response = requests.get(self.url, headers=self.headers, params=self.querystring)

        # print(self.response.json())