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
        job_type = "intern" if "Internship" in query else None
        self.querystring = {"query": f"{query}","page":"1","num_pages":"1","date_posted": "week", "employment_types": job_type}

        self.headers = {
            "X-RapidAPI-Key": os.environ['RAPID_API_KEY'],
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

        self.response = requests.get(self.url, headers=self.headers, params=self.querystring)
        # print(self.response.json())
        self.datas = self.response.json().get('data')
        # print(self.response.json())

    def get_job(self) -> list[dict]:
        jobs = []
        for data in self.datas:
            jobs.append(self._format(data))
        return jobs
            
    
    def _format(self, data) -> dict:
        return {
            "employer_name": data.get('employer_name'),
            "employer_logo": data.get('employer_logo'),
            "employer_website": data.get('employer_website'),
            "job_employment_type": data.get('job_employment_type'),
            "job_title": data.get('job_title'),
            "job_apply_link": data.get('job_apply_link'),
            "job_description": data.get('job_description'),
            "job_city": data.get('job_city'),
            "job_state": data.get('job_state'),
            "job_responsibilities": data.get('job_highlights').get("Responsibilities"),
            "job_qualifications": data.get('job_highlights').get("Qualifications")

        }

        # print(
        #     employer_name,
        #     employer_logo,
        #     employer_website,
        #     job_employment_type,
        #     job_title,
        #     job_apply_link,
        #     job_description,
        #     job_city,
        #     job_state,
        #     "\n"
        # )
