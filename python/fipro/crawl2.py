# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import bs4

drvdir = "/project/02_Software/webdrivers/chromedriver"

driver = webdriver.Chrome(drvdir)

url = 'https://www.instagram.com/explore/tags/'
tag = '부평역맛집'
endcount = 10

driver.get(url+tag)
time.sleep(5)
driver.find_element_by_class_name('_9AhH0').click()

time.sleep(5)
    
startcount=0

while True:
    startcount += 1
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'html.parser')
    print(type(bs))
    like = bs.find('div', class_='Nm9Fw').find('span').text
    print(like)
    name = bs.find('h2', class_='_6lAjh').text
    print(name)
    content = bs.find('div', class_='C4VMK').find('span').text
    print(content)


    for i in bs.select('.C4VMK span a'):
        print(i.text)
    source=""
    bs=""
    like=""
    name=""
    content=""
    time.sleep(5)

    driver.find_element_by_xpath("//a[@class='HBoOv coreSpriteRightPaginationArrow']").click()
    if startcount == endcount:
        break

print(type(source))



        
        