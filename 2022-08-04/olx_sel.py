from selenium import webdriver
from selenium.webdriver.common.by import By
import time
PATH = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(PATH)
# headers = {
#     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
# }
base_url = "https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723?page="
print(driver.title)
for page in range(1, 3):
    next_page = base_url + str(page)
    pages = driver.get(next_page)
    time.sleep(5)
    print(next_page)

    li_tag = driver.find_elements(
        By.XPATH, "//ul[@data-aut-id='itemsList']/li/a")
    links = len(li_tag)
    print(links)
    for i in range(links):
        time.sleep(4)
        property_links = driver.get(li_tag[i].get_attribute('href'))

        print(property_links)
        # time.sleep(10)
        # property_links.click()

driver.quit()
