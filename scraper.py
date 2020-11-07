from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re
import logging
import traceback

options = Options()
driver = webdriver.Chrome()

url = "https://www.google.com/maps/place/UPA+24h+Boa+Vista/@-25.3857065,-49.2350658,17z/data=!3m1!4b1!4m5!3m4!1s0x94dce66f6ff5ece5:0x1b92d4f7158c1e76!8m2!3d-25.3857065!4d-49.2328771"

driver.get(url)

wait = WebDriverWait(driver, 10)

response = BeautifulSoup(driver.page_source, 'html.parser')
rlist = response.find_all('div', class_='section-review-content')

for r in rlist:
    try:
        review_text = r.find('span', class_='section-review-text').text
    except Exception:
        review_text = None

    print(review_text)
    print(10*'-')

# Scroll não funcionando
scrollable_div = driver.find_element_by_css_selector(
 'div.section-layout.section-scrollbox.scrollable-y.scrollable-show'
                     )
driver.execute_script(
               'arguments[0].scrollTop = arguments[0].scrollHeight', 
                scrollable_div
               )