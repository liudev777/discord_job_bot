import requests

# url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Software%2BEngineer&location=United%2BStates&locationId=&geoId=103644278&f_TPR=&f_PP=103112676&start=0'

url = 'https://www.linkedin.com/jobs/view/junior-software-engineer-at-supernova-technology%E2%84%A2-3661572046?refId=uhTpcq0l%2F51Kgwnf5xEmaQ%3D%3D&trackingId=Ya%2F8U2oD%2BL3yrRQ17e4kHw%3D%3D&position=4&pageNum=0&trk=public_jobs_jserp-result_search-card'

proxy = '45.152.188.241:3128'
proxies = {'http': proxy, 'https': proxy}
# proxies = None

ip = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=3)
print(ip.json())

try:
    r = requests.get(url, proxies=proxies, timeout=3)
    # print(r.text)
    with open('linkedin_out2.html', 'w') as f:
        print(r.text, file=f)
except Exception as e:
    print("Something went wrong: ", e)