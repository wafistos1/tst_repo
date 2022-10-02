from ast import While
from PIL import Image
from pytesseract import pytesseract
import logging
import time
import os
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent
import urllib.request

IMAGE_NAME = 'captcha.jpg'

urllib.request.urlretrieve("https://sandbox.dereuromark.de/captcha/captcha/display/28566", "local-filename.jpg")
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)



# LUNCH BROWSER
logging.info('Extract image captcha from server.')
options = Options()
ua = UserAgent()
userAgent = ua.random
logging.info(userAgent)
options.add_argument(f'user-agent={userAgent}')
#options.add_argument("--headless")
driver = webdriver.Firefox(options=options, executable_path='./geckodriver')
driver.get('https://sandbox.dereuromark.de/sandbox/captchas/math')
logging.info('Browser lunched..')

count = 0

while True:
    
    driver.get('https://sandbox.dereuromark.de/sandbox/captchas/math')
    
    try:
        # 1 Extract image link
        body = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))


        # 2 Save image from server
        r = body.get_attribute('innerHTML')
        time.sleep(0.5)
        soup = BeautifulSoup(r, "html.parser")
        image_link = soup.find('form').find('img')['src'].split('.png')[0]
        print('image_link', image_link)
        urllib.request.urlretrieve(image_link, IMAGE_NAME)
        logging.info('Image seved at %s', IMAGE_NAME)


        # 3 extract text from image
        logging.info('Extract text from image')
        def img_to_text(path_to_image):
            try:
                img = Image.open(path_to_image)
                pytesseract.run_tesseract.tesseract_cmd = r"/usr/bin/tesseract"
                text = pytesseract.image_to_string(img, config='--psm 6')
                return text
            except:
                return 'None'
        text = img_to_text(IMAGE_NAME)
        logging.info('Text extract %s', text)


        # 4 resolve equation
        regex = re.compile(r'(?P<left>\d*\.?\d*)(?P<eq>[-+\/*()])(?P<right>\d*\.?\d*)')
        p = re.match(regex, text)
        left, right, equation = int(p['left']), int(p['right']), p['eq']
        print(left, equation, right)
        if equation == '+':
            result = left + right
        elif equation == '-':
            result = left - right
        logging.info('Equation resolve result = %s', result)
        time.sleep(10)


        # 5 send equation to form
        logging.info('Send equation to form')
        driver.find_element(By.XPATH, '//input[@id="name"]').send_keys('chien')
        driver.find_element(By.XPATH, '//input[@id="captcha-result"]').send_keys(result)
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()


        # 6 Check if Captch is resolved
        body = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
        r = body.get_attribute('innerHTML')
        soup = BeautifulSoup(r, "html.parser")
        message = soup.find('div', {'class': 'alert'}).text.strip()
        if message != 'The animal could not be saved. Please, try again.':
            logging.info('Captcha is Resolved and Task is finished..')
            break
    except:
        count =+ 1
        pass
    # return result




