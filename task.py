from bs4 import BeautifulSoup as bs
from selenium import webdriver
import numpy as np
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from algoliasearch.search_client import SearchClient
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
s=ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=chrome_options)

id = []
title = []
price = []
currency = []
description = []
colors = []
category = []
size = []
links = []
slug = []
url = []
pages = np.arange(1, 2)
driver.get('https://www.rimowa.com/fr/en/all-accessories')
time.sleep(0.5)

for p in pages:
    time.sleep(1)
    soup = bs(driver.page_source, 'html.parser')
    products = soup.find_all('a', class_='product-link')
    for product in products:
        soup = bs(driver.page_source, 'html.parser')
        links.append('https://www.rimowa.com/fr/en/accessories' + product['href'])
        slug.append(product['href'].replace('https://www.rimowa.com/fr/en/accessories/', ''))

for link in links:
    driver.get(link)
    time.sleep(1)
    soup1 = bs(driver.page_source, 'html.parser')
    iD = driver.find_element(By.XPATH,'/html/body/div[1]/div[5]/div[2]')
    idd = iD.get_attribute('data-pid')
    id.append(idd)
    title.append(soup1.find('span', attrs={'class': 'full-name'}).text.replace('\n', ' '))
    currency.append(soup1.find('span', attrs={'class': 'price-nocents'}).text.split()[1].replace('\n',' ').strip())
    price.append(soup1.find('span', attrs={'class': 'price-nocents'}).text.split()[0].replace('\n',' ').strip())
    description.append(soup1.find('div', attrs={'class': 'product-description'}).text.strip())
    category.append(soup1.find('a', attrs={'class': 'js-pdp-breadcrumb'}).text.strip())
    sub_category=soup1.find('h2', attrs={'class': 'js-product-collection'}).text.strip()
    img_url = soup1.find('img', attrs={'class': 'js-first-pdp-img'})
    url.append('https://www.rimowa.com'+ img_url['src'])
    metric = soup1.find('details', attrs={'class': 'metric'})
    if metric is not None:
        size.append(soup1.find('span', attrs={'class': 'metric'}).text.strip())
    if sub_category == 'Stickers':
        size.append('10.5 x 14.7 cm')
    else:
        size.append('unavailable')
    print(id)
    print(title)
    print(currency)
    print(description)
    print(price)
    print(url)
    print(slug)
    print(category)
    print(size)

time.sleep(3)
driver.close()
driver.quit()


products_data = []

for i in range(len(title)):
    product = {
         'id': id[i],
         'title': title[i],
         'currency':currency[i],
         'price': price[i],
         'description': description[i],
         'images': [
              {
                'url': url[i],
                'size': size[i],
              }],
         'category': category[i],
         'slug': slug[i],
         'objectID': id[i],


    }
    products_data.append(product)


client = SearchClient.create('OTJIXT29HV', '27df35ff75e8121489163e5cec0882ff')
index = client.init_index("dev_test")

for item in products_data:
    index.save_object(item, {'autoGenerateObjectIDIfNotExist': True})



