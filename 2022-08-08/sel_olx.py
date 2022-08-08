from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
PATH = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(PATH)
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
property_link = []
# properties_detail = []
base_url = "https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723?page="


def crawl(url):
    # driver.implicitly_wait(20)

    for page in range(1, 2):
        next_page = base_url + str(page)
        pages = driver.get(next_page)
        time.sleep(5)
        # print(next_page)

        li_tag = driver.find_elements(
            By.XPATH, "//ul[@data-aut-id='itemsList']/li/a")

        links = len(li_tag)
        # print(links)
        time.sleep(5)

        for i in range(links):

            property_link.append(li_tag[i].get_attribute('href'))
        for properties in property_link:
            print(properties)

            driver.execute_script("window.open('" + properties + "');")
            house_properties = driver.switch_to.window(
                driver.window_handles[1])
            time.sleep(10)
            response(house_properties)


def response(house_properties):

    property_id = (driver.find_element(By.XPATH, "//div/strong[contains(text(),'AD ID')]"
                                       ).text).lstrip("AD ID")

    list1 = driver.find_element(By.XPATH, "//span[@data-aut-id='itemPrice']"
                                ).text
    convert_list = list1.split(' ')
    for price_dict in range(len(convert_list)):

        price_dict = {'amount': convert_list[0]}
    price_dict = {
        'amount': convert_list[-1],
        'currency': convert_list[0]
    }

    bathroom = driver.find_element(By.XPATH, "//div/span[@data-aut-id='value_bathrooms']"
                                   ).text
    bathrooms = 0 if bathroom is None else ''.join(
        bathrooms for bathrooms in bathroom if bathrooms.isdigit())

    bedroom = driver.find_element(By.XPATH, "//div/span[@data-aut-id='value_rooms']"
                                  ).text

    bedrooms = 0 if bedroom is None else ''.join(
        bedrooms for bedrooms in bedroom if bedrooms.isdigit())

    properties_detail = {
        'property name': driver.find_element(By.XPATH, "//h1[@data-aut-id='itemTitle']"
                                             ).text,
        'property id': int(property_id),
        'breadcrumbs': [crumbs.text for crumbs in driver.find_elements(By.XPATH, "//div[@data-aut-id='breadcrumb']/div/ol/li/a"
                                                                       )],
        'price': price_dict,
        'img': WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//figure/img[@class='_39P4_']"))).get_attribute('src'),
        'description': driver.find_element(By.XPATH, "//div[@data-aut-id='itemDescriptionContent']/p"
                                           ).text,
        'seller_name': driver.find_element(By.XPATH, "//div[@data-aut-id='profileCard']/div/a/div"
                                           ).text,
        'location': driver.find_element(By.XPATH, "//div[@data-aut-id='itemLocation']/div/span"
                                        ).text,
        'property_type': driver.find_element(By.XPATH, "//div/span[@data-aut-id='value_type']"
                                             ).text,
        'bathroom': int(bathrooms),
        'bedrooms': int(bedrooms),
    }
    print(properties_detail)
    time.sleep(5)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


crawl(base_url)
