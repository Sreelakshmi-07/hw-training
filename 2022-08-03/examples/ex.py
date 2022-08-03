import selenium
from selenium import webdriver 
PATH = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(PATH)
driver.get("https://www.techwithtim.net/")
driver.quit()