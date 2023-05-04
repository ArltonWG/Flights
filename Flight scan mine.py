from time import sleep, strftime
from random import randint
import pandas as pd

#Selenium
from selenium.webdriver.common.by import By
from selenium import webdriver    
import chromedriver_autoinstaller
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
chromedriver_autoinstaller.install()
driver = webdriver.Chrome(service=Service(),options=options)

driver.implicitly_wait(60) #Wait for the loading page
###Selenium End### 

def num_convert(price):
    return price.strip('$').replace(',','')

def start_kayak(city_from, city_to, date_start, date_end):
    """City codes - it's the IATA codes!
    Date format -  YYYY-MM-DD"""
    
    kayak = ('https://www.kayak.com/flights/' + city_from + '-' + city_to +
             '/' + date_start + '-flexible/' + date_end + '-flexible?sort=bestflight_a')
    driver.get(kayak)
    sleep(randint(2,3))

    #prices
    xp_sections = 'jPY1-inner'
    sections = driver.find_elements(By.CLASS_NAME, xp_sections)
    sections_list = [value.text for value in sections]
    for section in sections_list:
        print(section)
    
    price_list = list(map(num_convert, sections_list))

    #dates
    dates_sections = 'VuLg'
    date_sections = driver.find_elements(By.CLASS_NAME, dates_sections)
    date_sections_list = [value.text for value in date_sections]
    for date_section in date_sections_list:
        print(date_section)

    #combine
    values = 49
    price_dict = [{'from_city': city_from, 'to_city': city_to} for _ in range(values)]
    for i in range(values):
        price_dict[i]['from_date'] = date_sections_list[i % 7]
        price_dict[i]['return_date'] = date_sections_list[i // 7 + 7]
        price_dict[i]['price'] = price_list[i]

    print(price_dict)
    cheapest = price_dict[price_list.index(min(price_list))]
    print('Cheapest flight from {} to {} leaves on {} and arrives on {} and costs {}'.format())

if __name__ == "__main__":
    #city_from = input('From which city? ')
    #city_to = input('Where to? ')
    #date_start = input('Search around which departure date? Please use YYYY-MM-DD format only ')
    #date_end = input('Return when? Please use YYYY-MM-DD format only ')

    city_from = 'LIS'
    city_to = 'SIN'
    date_start = '2023-08-21'
    date_end = '2023-09-07'

    start_kayak(city_from, city_to, date_start, date_end)

    # Bonus: save a screenshot!
    driver.save_screenshot('pythonscraping.png')