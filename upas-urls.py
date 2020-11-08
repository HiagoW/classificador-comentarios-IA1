from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
from bs4 import BeautifulSoup

url_upa_search = "https://www.google.com.br/maps/search/upa/@-25.4473693,-49.2466962,12z"
 
driver = webdriver.Chrome()
driver.get(url_upa_search)
 
wait = WebDriverWait(driver, 10)
 
time.sleep(5)
 
response = BeautifulSoup(driver.page_source, 'html.parser')
upasDivs = []
upasDivs = response.find_all('div', class_='section-result-title-container')
 
upas_names = []
 
for divs in upasDivs:
   upas_names = divs.find('h3', class_='section-result-title').text
   print(upas_names)