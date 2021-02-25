from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
import re
import io

upas_urls = []

read = open("upas.txt", 'r')
i = 0
for line in read:
    upas_urls.append(line)

read.close() 

reviews = []
driver = webdriver.Chrome()

for url in upas_urls:

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 10)

        time.sleep(5)

        # Pega div dos comentarios
        pane = driver.find_elements_by_xpath(
                                            '//div[@class=\'section-layout section-scrollbox scrollable-y scrollable-show\']')[0]
        # Pega altura do scroll
        last_height = pane.get_attribute("scrollHeight")

        while True:
            # Faz o scroll até o último review
            last_review = driver.find_elements_by_xpath(
                                            '//div[@class=\'section-review ripple-container GLOBAL__gm2-body-2\']')[-1]
            driver.execute_script('arguments[0].scrollIntoView(true);', last_review)

            time.sleep(3)

            # Nova altura do scroll
            new_height = pane.get_attribute("scrollHeight")

            # Pega ultimo comentario
            response = BeautifulSoup(driver.page_source, 'html.parser')
            ultimaDivComentario = response.find_all('div', class_='section-review-content')[-1]

            ''' Se o ultimo comentario for vazio, pode dar break pq começam 
            a aparecer apenas avaliações sem comentários '''

            try:
                review_text = ultimaDivComentario.find('span', class_='section-review-text').text
                if review_text.strip() == "":
                    break
            except Exception:
                break

            ''' Se a altura do scroll for igual a anterior, não tem mais 
            reviews para carregar '''

            if new_height == last_height:
                break

            last_height = new_height

        response = BeautifulSoup(driver.page_source, 'html.parser')
        rlist = response.find_all('div', class_='section-review-content')

        for r in rlist:

            # Salva a qtd de estrelas
            rating = r.find('span', class_='section-review-stars')['aria-label']
            rating = re.sub("[^0-9]", "", rating)
            rating = int(rating)
            # Reclassificação: 1 - Positivo; 0 - Negativo; -1 - Indeterminado
            if rating == 5:
                rating = 1
            elif rating == 1 or rating == 2:
                rating = 0
            else:
                rating = -1

            # Salva comentario se não for
            try:
                review_text = r.find('span', class_='section-review-text').text
                if review_text.strip() != "":
                    reviews.append((rating,review_text))
            except Exception:
                review_text = None
    except Exception:
        continue

with io.open('output.csv','w',newline='\n',encoding="utf-8") as result_file:
    csv_out=csv.writer(result_file, delimiter=';')
    csv_out.writerow(['classificacao','texto'])
    for row in reviews:
        csv_out.writerow(row)
