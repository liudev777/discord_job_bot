from pprint import pp
import requests
from bs4 import BeautifulSoup

class Linkedin:
    def __init__(self, location_name=None, position=None):
        self.proxies = self._establish_connection()
        self.f_PP = self._fetch_f_PP(location_name)
        self.f_E = self._fetch_f_E(position)
        self.url = f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Software%2BEngineer&location=United%2BStates&locationId=&geoId=103644278&f_TPR=r604800&f_PP={self.f_PP}&f_E={self.f_E}&start='
        self.job_list = []

    # grabs the location_id from linkedin
    def _fetch_f_PP(self, location_name):
        if not self.proxies:
            return None

        if not location_name:
            return None
        url = f'https://www.linkedin.com/jobs-guest/api/typeaheadHits?origin=jserp&typeaheadType=GEO&geoTypes=POPULATED_PLACE&query={location_name}'
        r = requests.get(url, proxies=self.proxies, timeout=3)
        f_PP = r.json()[0].get("id")
        return f_PP
    
    def _fetch_f_E(self, position):
        if not self.proxies:
            return None
    
        if not position:
            return None
        
        positions = {
            "internship": "1",
            "junior": "2%2C3%2C4",
            "senior": "5"
        }
        return positions.get(position)


    def _parse_html(self, html) -> list:
        soup = BeautifulSoup(html, 'html.parser')
        jobs = []

        for card in soup.find_all('div', class_='base-search-card'):
            # Extract job link
            job_link_tag = card.find('a', class_='base-card__full-link')
            job_link = job_link_tag['href'] if job_link_tag else None

            # Extract job name/title
            job_title_tag = card.find('h3', class_='base-search-card__title')
            job_title = job_title_tag.get_text(strip=True) if job_title_tag else None

            # Extract company name
            a_tag = card.find('a', class_='hidden-nested-link')
            company_name = a_tag.get_text(strip=True) if a_tag else None

            # Extract job image data-delayed-url
            job_image_tag = card.find('img', class_='artdeco-entity-image')
            job_image_url = job_image_tag['data-delayed-url'] if job_image_tag and 'data-delayed-url' in job_image_tag.attrs else None

            jobs.append({
                "job_link": job_link,
                "job_title": job_title,
                "company_name": company_name,
                "job_image_url": job_image_url  # the extracted data-delayed-url
            })

        return jobs


    def _extend_jobs(self):
        if not self.proxies:
            print("No proxie provided")
            return 
        
        for n in range(0, 1, 25):
            url = self.url + str(n)
            try:
                html = requests.get(url, proxies=self.proxies, timeout=3)
                self.job_list.extend(self._parse_html(html.text))
            except Exception as e:
                print("Something went wrong: ", e)

    def get_job_list(self) -> list:
        self._extend_jobs()
        return self.job_list
    
    def _establish_connection(self):
        proxy = '2.56.119.93:5074'
        proxies = {'http': f'socks5://{proxy}', 'https': f'socks5://{proxy}'}
        
        # Use a session for better performance
        with requests.Session() as session:
            try:
                return proxies
                response1 = session.get('https://httpbin.org/ip', proxies=proxies, timeout=10)
                
                # Check status code as an integer
                if response1.status_code == 200:
                    print(response1.json())
                    # Assuming Linkedin is a class and get_job_list is a method
                    return proxies
                else:
                    print(response1.status_code)
                    
            except requests.exceptions.ProxyError:
                print("Proxy Error. Check if your proxy is valid.")
            except requests.exceptions.Timeout:
                print("Request timed out.")
            except requests.exceptions.ConnectionError:
                print("Connection Error.")
            except Exception as e:
                print("An error has occurred:", e)
                raise e
        return None


if __name__ == "__main__":
    jobs = Linkedin(location_name="chicago", position="internship").get_job_list()
    pp(jobs)