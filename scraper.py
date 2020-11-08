from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
import re
import io

urls = \
    [\
    "https://www.google.com/maps/place/UPA+24h+Boa+Vista/@-25.3857065,-49.2350658,17z/data=!4m7!3m6!1s0x94dce66f6ff5ece5:0x1b92d4f7158c1e76!8m2!3d-25.3857065!4d-49.2328771!9m1!1b1",\
    "https://www.google.com/maps/place/UPA+Maracan%C3%A3/@-25.3614534,-49.1915863,17z/data=!4m7!3m6!1s0x0:0x8954c9bb8097d648!8m2!3d-25.3614534!4d-49.1893976!9m1!1b1"\
    ]

reviews = []

for url in urls:

    driver = webdriver.Chrome()
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
        
        # Salva comentario se não for
        try:
            review_text = r.find('span', class_='section-review-text').text
            if review_text.strip() != "":
                reviews.append((rating,review_text))
        except Exception:
            review_text = None

with io.open('output.csv','w',newline='\n',encoding="utf-8") as result_file:
    csv_out=csv.writer(result_file, delimiter=';')
    csv_out.writerow(['classificacao','texto'])
    for row in reviews:
        csv_out.writerow(row)
