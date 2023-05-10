import os
import time
import requests
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.webdriver import By
from PIL import Image
from pytesseract import pytesseract
from annotations import tesseract_path_annotation, address_annotation, return_annotation


def extract_info(
    tesseract_path: tesseract_path_annotation,
    address: address_annotation
) -> return_annotation:

    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)

    driver.get(
        "https://www.ura.gov.sg/maps/"
        )

    time.sleep(1)

    driver.find_element(
        by=By.XPATH, 
        value='//*[@id="us-c-ip"]/div[1]/div[1]/div[4]/div[3]/div[4]/div[1]/img'
        ).click()

    time.sleep(1)

    driver.find_element(
        by=By.XPATH, 
        value='//*[@id="us-map-filter"]'
        ).click()

    time.sleep(1)

    driver.find_element(
        by=By.XPATH, 
        value='//*[@id="us-ip-cp-LHA-label"]/div[3]/label/span'
        ).click()

    driver.find_element(
        by=By.XPATH, 
        value='//*[@id="us-ip-cp-BH-label"]/div[3]/label/span'
        ).click()

    driver.find_element(
        by=By.XPATH, 
        value='//*[@id="us-f-footerclose"]'
        ).click()

    time.sleep(1)

    address_input = driver.find_element(
        by=By.XPATH, 
        value='//*[@id="us-s-txt"]'
        )

    address_input.send_keys(address)

    time.sleep(1)

    full_address = driver.find_element(
        by=By.XPATH, 
        value='/html/body/div[6]/div[2]/div/a/div[2]'
        ).text

    driver.find_element(
        by=By.XPATH, 
        value='/html/body/div[6]/div[2]/div/a'
        ).click()

    time.sleep(1)

    driver.find_element(
        by=By.XPATH, 
        value='//*[@id="us-map"]/div[3]/div[3]/div[2]/a[1]'
        ).click()

    time.sleep(1)

    driver.find_element(
        by=By.XPATH, 
        value='//*[@id="us-map"]/div[3]/div[3]/div[2]/a[1]'
        ).click()

    time.sleep(1)

    img_location = driver.find_element(
        by=By.XPATH, 
        value='//*[@id="us-map"]/div[2]/div[4]/img'
        ).location

    x = img_location['x']
    y = img_location['y']
    width = x + 200
    height = y + 80

    img = driver.find_element(
        by=By.XPATH, 
        value='//*[@id="us-map"]/div[2]/div[3]/img[1]'
        )

    img_url = img.get_attribute('src')
    img_url = img_url.replace('=show%3A0', '=show%3A1')

    headers = {"User-Agent": "a user agent"}
    response = requests.get(img_url, stream=True, headers=headers)
    if response.status_code == 200:
        with open(f'ss{address}.png','wb') as f:
            shutil.copyfileobj(response.raw, f)
    
    image = Image.open(f'ss{address}.png')

    image = image.crop((x-200, y-20, width, height))

    # image.save(f'snap{address}.png')

    pytesseract.tesseract_cmd = tesseract_path

    text = pytesseract.image_to_string(image)
    text = text.replace("\n", " ")
    text = text.rstrip()

    data = {
        'address/pincode': full_address,
        'information': text
    }

    return data
