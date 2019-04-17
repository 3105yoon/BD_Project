from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import threading
import datetime
import csv

startTime = time.time() 
# 코드 실행 시간 측정(시작시간)

options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values': {'cookies'                   : 2, 'images': 2,
                                                    'plugins'                   : 2, 'popups': 2, 'geolocation': 2,
                                                    'notifications'             : 2, 'auto_select_certificate': 2,
                                                    'fullscreen'                : 2,
                                                    'mouselock'                 : 2, 'mixed_script': 2,
                                                    'media_stream'              : 2,
                                                    'media_stream_mic'          : 2, 'media_stream_camera': 2,
                                                    'protocol_handlers'         : 2,
                                                    'ppapi_broker'              : 2, 'automatic_downloads': 2,
                                                    'midi_sysex'                : 2,
                                                    'push_messaging'            : 2, 'ssl_cert_decisions': 2,
                                                    'metro_switch_to_desktop'   : 2,
                                                    'protected_media_identifier': 2, 'app_banner': 2,
                                                    'site_engagement'           : 2,
                                                    'durable_storage'           : 2}}
options.add_experimental_option('prefs', prefs)
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")


drvdir = "/project/02_Software/webdrivers/chromedriver" 

driver = webdriver.Chrome(drvdir, chrome_options=options) 


starturl = 'https://www.instagram.com/explore/tags/' 
# 태그 검색 url
keyword = '연남동' 
# 검색하고 싶은 태그 (추후 입력받게끔 해야함)
 
# 크롤링 횟수 (추후 입력받게끔 해야함)

driver.get(starturl+keyword) 
# 검색하고 싶은 태그 검색
time.sleep(5) 
# 브라우저 실행 후 기다려줘야하는 최소 시간

endcount = 10000

alt_list = []


def geturl():
    global alt_list
    html = driver.page_source 
    # 접속한 페이지 소스 load
    soup = BeautifulSoup(html, 'html.parser') 
    #react-root > section > main > article > div.EZdmt > div > div > div:nth-child(1) > div:nth-child(3) > a
    for i in soup.select('.EZdmt > div > div > div > div > a'):
        addr = "https://www.instagram.com" + i['href']
        alt_list.append(addr)
    #react-root > section > main > article > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(1) > a
    for i in soup.select('div:nth-child(3) > div > div > div > a'):
        addr = "https://www.instagram.com" + i['href']
        alt_list.append(addr)
        
def geturl3():
    global alt_list
    html2 = driver.page_source 
    # 접속한 페이지 소스 load
    soup2 = BeautifulSoup(html2, 'html.parser') 
    #react-root > section > main > article > div:nth-child(3) > div > div:nth-child(1) > div:nth-child(1) > a
    for i in soup2.select('div:nth-child(3) > div > div > div > a'):
        addr = "https://www.instagram.com" + i['href']
        if addr not in alt_list[-33]:
            alt_list.append(addr)
    

def thread_run():
    #while True:
    elem = driver.find_element_by_tag_name("body")
    elem.send_keys(Keys.HOME)
    print("thread execute!") 
        
    threading.Timer(30, thread_run).start()
        
 
    
def main():
    global alt_list
    geturl()
    thread_run()

    while True:
        alt_list = list(set(alt_list))  #중복제거
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        geturl3()
        print(len(alt_list))
        if len(alt_list) >= endcount:
            alt_list = alt_list[:endcount]
            break
        else:
            continue
    
    driver.close()
    
    now = datetime.datetime.now()
    filename = keyword+'_%s.csv' % now.strftime('%Y-%m-%d %H:%M:%S')
    csvfile = open('./datalist/' + filename, 'w')
    reader = csv.writer(csvfile)
    for save in range(len(alt_list)):
        data = alt_list[save].split(",")
        reader.writerow(data)
    endTime = time.time() - startTime
    print('걸린 시간은 : ',endTime) 



main()
        