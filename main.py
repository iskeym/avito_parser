import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By

def link(driver, links, page, u):
    url = (f'{u}&p={page}')
    driver.get(url)

    items = driver.find_elements(By.CLASS_NAME, "js-catalog-item-enum")
    for item in items:
        link = item.find_element(By.CLASS_NAME, "title-root_maxHeight-X6PsH").get_attribute('href')
        links.append(link)

def info(driver, total, links):
    for link in links:
        driver.get(link)

        x = []
        x.append({
            'title': driver.find_element(By.XPATH, "//span[@class='title-info-title-text']").text,
            'price': driver.find_element(By.XPATH, "//span[@class='js-item-price']").text,
            'address': driver.find_element(By.XPATH, "//span[@class='item-address__string']").text,
            'name': driver.find_element(By.XPATH, "//div[@class='seller-info-name js-seller-info-name']//a").text,
            'articul': driver.find_element(By.XPATH, "//span[@data-marker='item-view/item-id']").text,
            'link': link
        })

        print(x)
        total.extend(x)

def save(total):
    with open('parser.csv', 'w', newline='') as ex:
        writer = csv.writer(ex, delimiter=';')
        writer.writerow(['название', 'цена', 'адрес', 'имя', 'номер товара', 'ссылка'])
        for dict in total:
            writer.writerow([dict['title'], dict['price'], dict['address'], dict['name'], dict['articul'], dict['link']])

def parser():
    driver = webdriver.Chrome()
    url = 'https://www.avito.ru/bratsk/avtomobili?cd=1&radius=200'
    pages = 1

    links = []
    for page in range(1, pages + 1):
        link(driver, links, page, url)

    print(links)

    total = []
    info(driver, total, links)

    print(total)

    save(total)
    os.startfile('parser.csv')

    driver.close()

parser()