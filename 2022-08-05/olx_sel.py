from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
PATH = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(20)
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}
property_link = []
base_url = "https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723?page="

property_link = []


def crawl(url):

    for page in range(1, 3):
        next_page = base_url + str(page)
        pages = driver.get(next_page)
        time.sleep(5)
        # print(next_page)
        driver.implicitly_wait(10) 
        li_tag = driver.find_elements(
            By.XPATH, "//ul[@data-aut-id='itemsList']/li/a")
        links = len(li_tag)
        print(links)
        time.sleep(5)

        for i in range(links):

            property_link.append(li_tag[i].get_attribute('href'))
            for property_links in property_link:
                properties_link = driver.get(property_links)

            response(properties_link)


def response(properties_link):

    # list1 = ' '.join(map(str,
    #                      driver.find_elements(By.XPATH, "//span[@data-aut-id='itemPrice']"
    #                                           ).text))
    # convert_list = list1.split(' ')
    # for price_dict in range(len(convert_list)):

    #     price_dict = {'amount': convert_list[0]}
    # price_dict = {
    #     'amount': convert_list[-1],
    #     'currency': convert_list[0]
    # }

    # bathroom = driver.find_elements(By.XPATH"//div/span[@data-aut-id='value_bathrooms']"
    #                                 ).text
    # bathrooms = 0 if bathroom is None else ''.join(
    #     bathrooms for bathrooms in bathroom if bathrooms.isdigit())

    # bedroom = driver.find_elements(By.XPATH, "//div/span[@data-aut-id='value_rooms']"
    #                                ).text

    # bedrooms = 0 if bedroom is None else ''.join(
    #     bedrooms for bedrooms in bedroom if bedrooms.isdigit())

    properties_detail = {
        'property name': driver.find_element(By.XPATH, "//h1[@data-aut-id='itemTitle']"
                                             ).text,
        # 'property id' : ' '.join(map(str,
        #                                    driver.find_elements(By.XPATH,"//div/strong[contains(text(),'AD ID')]"
        #                                                             ).re(r"\d+"))),
        # ).re(r"\d+"))),
        'breadcrumbs': driver.find_element(By.XPATH, "//div[@data-aut-id='breadcrumb']/div/ol/li/a"
                                           ).text,
        # 'price': price_dict,
        # 'img': driver.find_element(By.XPATH, "//figure/img[@class='_39P4_']"
        #                            ).get_attribute('href'),
        'description': driver.find_element(By.XPATH, "//div[@data-aut-id='itemDescriptionContent']/p"
                                           ).text,
        'seller_name': driver.find_element(By.XPATH, "//div[@data-aut-id='profileCard']/div/a/div"
                                           ).text,
        'location': driver.find_element(By.XPATH, "//div[@data-aut-id='itemLocation']/div/span"
                                        ).text,
        'property_type': driver.find_element(By.XPATH, "//div/span[@data-aut-id='value_type']"
                                             ).text,
        # 'bathroom': int(bathrooms),
        # 'bedrooms': int(bedrooms),
        }
    print(properties_detail)

    time.sleep(2)



crawl(base_url)
