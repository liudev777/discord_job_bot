from bs4 import BeautifulSoup
# from requests_html import HTMLSession
import requests
from playwright.sync_api import sync_playwright

# proxy = "34.87.130.147:8080"

url = "https://neetcode.io/practice"
url2 = "https://leetcode.com/problems/substring-with-largest-variance/"
url3 = "https://neetcode.io/main.e9d3b0a379eb0fd4.js"

# session = HTMLSession()

try:
    response1 = requests.get('https://httpbin.org/ip', timeout=3)
    print(response1.json())
except Exception as e:
    print(e)

try:
    # with sync_playwright() as p:
    #     browser = p.chromium.launch()
    #     page = browser.new_page()
    #     page.goto(url)
    #     # with open('output4.html', 'w') as f:
    #     #     f.write(page.content())
    #     accordion_button = page.locator("button.accordion").nth(1)
    #     accordion_button.click()
    #     row_locator = page.locator("tr").filter(has_text="3Sum")
    #     # row_locator.filter(has_text="3Sum")
    #     print(row_locator.get_attribute("class"))
    #     buttons = row_locator.locator('a#discord-gray').first
    #     print(buttons)
    #     buttons.click()
    #     # with open('output5.html', 'w') as f:
    #     #     f.write(page.content())
    #     modal = page.locator('.modal.is-active.ng-star-inserted.dialog-open')
    #     print(modal)
    #     youtube = modal.get_by_text('View on Youtube')
    #     print(youtube.get_attribute('href'))
    #     browser.close()

        with sync_playwright() as p:
            browser = p.chromium.launch()
            page= browser.new_page()
            page.goto(url)
            for category in page.locator("div.accordion-container").all():
                print('category', category.locator("p").first.inner_text())
                category_button = category.locator("button").first
                # category_button.click()
                rows = category.locator("tbody").locator("tr.ng-star-inserted").all()
                print([row.locator("a.table-text").inner_text() for row in rows])
                for row in rows:
                    title_tag = row.locator("td a.table-text").first
                    title = title_tag.inner_text()
                    print("title: ", title)
                    buttons = row.locator('a#discord-gray').first
                    buttons.click()
                    modal = page.locator('.modal.is-active.ng-star-inserted.dialog-open')
                    youtube = modal.get_by_text('View on Youtube')
                    print(youtube.get_attribute('href'))
                    close = modal.get_by_role("button")
                    print("close", close.locator("b").inner_text())
                    close.click()
            browser.close()
except Exception as e:
    print("timed out\n", e, "\n")