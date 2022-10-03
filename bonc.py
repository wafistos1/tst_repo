from playwright.sync_api import sync_playwright
import time
import pandas as pd
from bs4 import BeautifulSoup
import re
# from utils import Driver, log, txt
import logging

logging.basicConfig( level=logging.INFO )#, filename='myapp.log')

df = pd.read_csv('model_product.csv')

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(' https://www.leboncoin.fr/recherche?locations=Paris__48.8495376581948_2.340572835508209_8691')

    time.sleep(0.5)
    page.locator('xpath=//button[@id="didomi-notice-agree-button"]').click()
    # annonces = page.locator('xpath=//div[@class="styles_adCard__HQRFN styles_classified__rnsg4"]')
    while True:
        time.sleep(2)
        r = page.inner_html('body')
        soup = BeautifulSoup(r, 'html.parser')
        # print(soup)
        # page.wait_for_timeout(10000)
        # #Captcha 
        annonces = soup.find_all('div', {'class': 'styles_adCard__HQRFN styles_classified__rnsg4'})
        print(len(annonces))
        data = []
        for annonce in annonces:
            try:
                data.append({   
                            'Title': annonce.find('p', {'data-qa-id': 'aditem_title'}).text.strip(),
                            'Price': annonce.find('p', {'data-test-id': 'price'}).text.strip(),
                            'Adresse': annonce.find('p', {'aria-label': re.compile(r'^Située')}).text.strip(),
                            'Date': annonce.find('p', {'aria-label': re.compile(r'^Date de dépôt')}).text.strip(),
                            'Categorie': annonce.find('p', {'aria-label': re.compile(r'^Catégorie')}).text.strip(),
                            })
            except:
                continue
        df1 = pd.DataFrame(data)
        df = pd.concat([df, df1], ignore_index=True)
        df.to_excel('Le_bon_coin_scrape.xlsx')
        #Click next 
        page.locator('xpath=//a[@title="Page suivante"]').click()
    time.sleep(160)
