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
url = "https://www.nykaa.com/natural/hair/conditioner/c/9599?root=nav_3&dir=desc&order=popularity"
product_links = []
img_links = []
def crawl(url):

	driver.get(url)
	product_list = driver.find_elements(By.XPATH,"//div[@class='css-d5z3ro']/a")
	links = len(product_list)
	# print(link)
	# print(product_list)
	for i in range(links):

		product_links.append(product_list[i].get_attribute('href'))
		# print(product_links)
	for products in product_links:

		driver.execute_script("window.open('"+products+"');")
		product_desc_page = driver.switch_to.window(driver.window_handles[1])
		time.sleep(10)
		response(product_desc_page)

def response(product_desc_page):


	
	product_details = {
		'product title' : driver.find_element(By.XPATH,"//h1[@class='css-1gc4x7i']").text.replace("\n", ""),
		'MRP' : driver.find_element(By.XPATH,"//span[@class='css-u05rr']").text,
		'offer price' : driver.find_element(By.XPATH,"//span[@class='css-1jczs19']").text,
		'offer' : driver.find_element(By.XPATH,"//span[@class='css-2w3ruv']").text,
		'ratings' : driver.find_element(By.XPATH,"//div[@class='css-1hvvm95']").text,
		'reviews' : driver.find_element(By.XPATH,"//div[@class='css-1hvvm95']").text,
		'img' : WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH,"//div[@class='css-ik61n6']/img"))).get_attribute('src')
	}
	print(product_details)

	driver.close()
	driver.switch_to.window(driver.window_handles[0])



crawl(url)