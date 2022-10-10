from playwright.sync_api import sync_playwright,Playwright
import re

def run(playwright: Playwright) -> None:

    browser = playwright.webkit.launch(headless=False)
    page = browser.new_page()
    # page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())
    page.route(re.compile(r"(\.png$)|(\.jpg$)|(\.js$)"), lambda route: route.abort())
    page.goto(
        'https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723')
    href = "//li[@data-aut-id='itemBox']/a"
    href_ = page.click(href)


    page.wait_for_timeout(6000)
    browser.close()

with sync_playwright() as playwright:
   run(playwright)

