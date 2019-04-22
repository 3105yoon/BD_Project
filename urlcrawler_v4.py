from selenium import webdriver
import time
from bs4 import BeautifulSoup
import threading
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


drvdir = "/project/03_Src/python/BD_Project/chromedriver" 

driver1 = webdriver.Chrome(drvdir, chrome_options=options) 


starturl = 'https://www.instagram.com/explore/tags/' 
# 태그 검색 url
time.sleep(5) 
# 브라우저 실행 후 기다려줘야하는 최소 시간

crawl_tag_list = []
crawl_count_list = []

print("Instagram Url Crawler")
print("태그에 '그만'을 입력하면 수집을 시작합니다.")
print("태그에 '확인'을 입력하면 현재 수집 목록을 보여드립니다.")




while True:
    tag = input("수집할 태그를 입력하세요 : ")
    
    if tag == "확인":
        for i in range(len(crawl_tag_list)):
                print("태그 :",crawl_tag_list[i], ", 횟수 : ", crawl_count_list[i])
        print("갯수 : ", len(crawl_tag_list))
    elif tag == "그만":
        break
    else:
        driver1.get(starturl+tag)
        time.sleep(1)
        driver1.implicitly_wait(1)
        try:
            totalcount = driver1.find_element_by_class_name('g47SY').text
        except:
            time.sleep(1)
            totalcount = driver1.find_element_by_class_name('g47SY').text
        print(tag, "은(는) 총 ", totalcount, "개의 게시글이 있네요.")
        crcount = int(input("몇 개 수집 할까요 ? : "))
        
        crawl_tag_list.append(tag)
        crawl_count_list.append(crcount)




def main1():
    url_list1 = []
    addr1 = ""
    upcount1 = 0
    tag1 = ""
    
            
    for i in range(len(crawl_tag_list)):
        print(crawl_tag_list[i], " 을 ", crawl_count_list[i], "개 수집 시작")
        driver1.get(starturl+crawl_tag_list[i]) 
        driver1.implicitly_wait(3)
        time.sleep(3)
        tag1 = crawl_tag_list[i]
        slicecount1 = crawl_count_list[i]
        while True:
            upcount1 += 1
        
            url_list1 = list(set(url_list1))  #중복제거
            driver1.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver1.implicitly_wait(1)
            time.sleep(1)
        
            html1 = driver1.page_source 
            soup1 = BeautifulSoup(html1, 'html.parser') 
            
            for i in soup1.select('.EZdmt > div > div > div > div > a'):
                addr1 = "https://www.instagram.com" + i['href']
                url_list1.append(addr1)
                for i in soup1.select('div:nth-child(3) > div > div > div > a'):
                    addr1 = "https://www.instagram.com" + i['href']
                    url_list1.append(addr1)
        
                
            if len(url_list1) >= slicecount1:
                url_list1 = url_list1[:slicecount1]
                break
            else:
                continue
    
        csvfile1 = open('./datalist/urllist/' + tag1 + '.csv' ,'w')
        reader1 = csv.writer(csvfile1)
        for save in range(len(url_list1)):
            data1 = url_list1[save].split(",")
            reader1.writerow(data1) 
        csvfile1.close()
        
def thread_run1():
    driver1.execute_script("window.scrollTo(0, 0);")
    driver1.implicitly_wait(1)
    time.sleep(1)
    print("thread execute!")
        
    threading.Timer(15, thread_run1).start() 

main1()

thread_run1()

driver1.close()

endTime = time.time() - startTime
print('끝났습니다. !! 걸린 시간은 : ',endTime) 