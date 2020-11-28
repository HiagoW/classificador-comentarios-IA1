from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time
from bs4 import BeautifulSoup

indexCurrentDiv = 0

url_upa_search = "https://www.google.com.br/maps/search/upa/@-25.4473693,-49.2466962,12z"
 
driver = webdriver.Chrome()
driver.get(url_upa_search)
 
wait = WebDriverWait(driver, 10)
 
time.sleep(5)
 

hasNextPage = 0
try:
   f = open("upasnames.txt", "a")
   f2 = open("upas.txt", "a")


   while (hasNextPage <= 1):
      upasDivs = driver.find_elements_by_class_name("section-result")
      upas_names = []
 
      while(indexCurrentDiv<len(upasDivs)):

         currentDiv = upasDivs[indexCurrentDiv]
         upas_names = currentDiv.find_element_by_class_name('section-result-title').text
         f.write(upas_names + "\n")

         driver.execute_script("arguments[0].click();", currentDiv)
         time.sleep(3)

         try:
            commentsButton = driver.find_element_by_class_name('allxGeDnJMl__button')
            driver.execute_script("arguments[0].click();", commentsButton)
            time.sleep(3)


            strUrl = driver.current_url
            f2.write(strUrl + "\n")
         except:
            pass

         while not driver.current_url.startswith('https://www.google.com.br/maps/search/upa/'):
            driver.execute_script("window.history.go(-1)")
            time.sleep(3)

         indexCurrentDiv+=1
         upasDivs = driver.find_elements_by_class_name("section-result")

      indexCurrentDiv=0
      nextPage = driver.find_element_by_xpath('//*[@id="n7lv7yjyC35__section-pagination-button-next"]')

      time.sleep(5)

      if (nextPage.is_enabled()):
         nextPage.click()
      else:
         hasNextPage +=1

except:
   print("erro")
finally:
   f.close()
   f2.close()

print("fim")

