from selenium import webdriver
import time
from bs4 import BeautifulSoup
#from selenium.webdriver.common.keys import Keys
import csv
from multiprocessing import Process
import threading

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

driver1 = webdriver.Chrome(drvdir, chrome_options=options)
driver2 = webdriver.Chrome(drvdir, chrome_options=options)
driver3 = webdriver.Chrome(drvdir, chrome_options=options)
driver4 = webdriver.Chrome(drvdir, chrome_options=options) 


starturl = 'https://www.instagram.com/explore/tags/' 
# 태그 검색 url
# 검색하고 싶은 태그 (추후 입력받게끔 해야함)
 
# 크롤링 횟수 (추후 입력받게끔 해야함)

# 검색하고 싶은 태그 검색
time.sleep(3) 
# 브라우저 실행 후 기다려줘야하는 최소 시간
crawl_tag_list = []
crawl_count_list = []

print("Instagram Url Crawler")
print("태그 4개 단위씩 입력해주세요.")
print("ex. 4, 8, 12 개의 태그")
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

length = int(len(crawl_tag_list)/4)

crawl_tag_list1 = crawl_tag_list[0:length]
crawl_tag_list2 = crawl_tag_list[length:length*2]
crawl_tag_list3 = crawl_tag_list[length*2:length*3]
crawl_tag_list4 = crawl_tag_list[length*3:]

crawl_count_list1 = crawl_count_list[0:length]
crawl_count_list2 = crawl_count_list[length:length*2]
crawl_count_list3 = crawl_count_list[length*2:length*3]
crawl_count_list4 = crawl_count_list[length*3:]
        


def main1():
    url_list1 = []
    addr1 = ""
    upcount1 = 0
    tag1 = ""
    slicecount1 = 0
    
            
    for i in range(len(crawl_tag_list1)):
        print(crawl_tag_list1[i], " 을 ", crawl_count_list1[i], "개 수집 시작")
        driver1.get(starturl+crawl_tag_list1[i]) 
        driver1.implicitly_wait(3)
        time.sleep(3)
        tag1 = crawl_tag_list1[i]
        slicecount1 = crawl_count_list1[i]
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
        
    def1 = False
        
    return def1
        
def main2():
    url_list2 = []
    addr2 = ""
    tag2 = ""
    slicecount2 = 0
    
    for i in range(len(crawl_tag_list2)):
        print(crawl_tag_list1[i], " 을 ", crawl_count_list1[i], "개 수집 시작")
        driver2.get(starturl+crawl_tag_list2[i]) 
        driver2.implicitly_wait(3)
        time.sleep(3)
        tag2 = crawl_tag_list2[i]
        slicecount2 = crawl_count_list2[i]
    
    
        while True:
        
            url_list2 = list(set(url_list2))  #중복제거
            driver2.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver2.implicitly_wait(1)
            time.sleep(1)
        
            html2 = driver2.page_source 
            soup2 = BeautifulSoup(html2, 'html.parser') 
            for i in soup2.select('.EZdmt > div > div > div > div > a'):
                addr2 = "https://www.instagram.com" + i['href']
                url_list2.append(addr2)
            for i in soup2.select('div:nth-child(3) > div > div > div > a'):
                addr2 = "https://www.instagram.com" + i['href']
                url_list2.append(addr2)
                
            if len(url_list2) >= slicecount2:
                url_list2 = url_list2[:slicecount2]
                break
            else:
                continue
    
        csvfile2 = open('./datalist/urllist/' + tag2 + '.csv' ,'w')
        reader2 = csv.writer(csvfile2)
        for save in range(len(url_list2)):
            data2 = url_list2[save].split(",")
            reader2.writerow(data2) 
        csvfile2.close()
        
        
def main3():
    url_list3 = []
    addr3 = ""
    tag3 = ""
    slicecount3 = 0
    
            
    for i in range(len(crawl_tag_list3)):
        print(crawl_tag_list1[i], " 을 ", crawl_count_list1[i], "개 수집 시작")
        driver3.get(starturl+crawl_tag_list3[i]) 
        driver3.implicitly_wait(3)
        time.sleep(3)
        tag3 = crawl_tag_list3[i]
        slicecount3 = crawl_count_list3[i]
    
    
        while True:
        
            url_list3 = list(set(url_list3))  #중복제거
            driver3.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver3.implicitly_wait(1)
            time.sleep(1)
        
            html3 = driver3.page_source 
            soup3 = BeautifulSoup(html3, 'html.parser') 
            for i in soup3.select('.EZdmt > div > div > div > div > a'):
                addr3 = "https://www.instagram.com" + i['href']
                url_list3.append(addr3)
            for i in soup3.select('div:nth-child(3) > div > div > div > a'):
                addr3 = "https://www.instagram.com" + i['href']
                url_list3.append(addr3)
        
            if len(url_list3) >= slicecount3:
                url_list3 = url_list3[:slicecount3]
                break
            else:
                continue
    
        csvfile3 = open('./datalist/urllist/' + tag3 + '.csv' ,'w')
        reader3 = csv.writer(csvfile3)
        for save in range(len(url_list3)):
            data3 = url_list3[save].split(",")
            reader3.writerow(data3) 
        csvfile3.close()
     
        
def main4():
    url_list4 = []
    addr4 = ""
    tag4 = ""
    slicecount4 = 0
    
    for i in range(len(crawl_tag_list4)):
        print(crawl_tag_list1[i], " 을 ", crawl_count_list1[i], "개 수집 시작")
        driver4.get(starturl+crawl_tag_list4[i]) 
        driver4.implicitly_wait(3)
        time.sleep(3)
        tag4 = crawl_tag_list4[i]
        slicecount4 = crawl_count_list4[i]
    
    
        while True:
        
            url_list4 = list(set(url_list4))  #중복제거
            driver4.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver4.implicitly_wait(1)
            time.sleep(1)
        
            html4 = driver4.page_source 
            soup4 = BeautifulSoup(html4, 'html.parser') 
            for i in soup4.select('.EZdmt > div > div > div > div > a'):
                addr4 = "https://www.instagram.com" + i['href']
                url_list4.append(addr4)
            for i in soup4.select('div:nth-child(3) > div > div > div > a'):
                addr4 = "https://www.instagram.com" + i['href']
                url_list4.append(addr4)
                
            if len(url_list4) >= slicecount4:
                url_list4 = url_list4[:slicecount4]
                break
            else:
                continue
    
        csvfile4 = open('./datalist/urllist/' + tag4 + '.csv' ,'w')
        reader4 = csv.writer(csvfile4)
        for save in range(len(url_list4)):
            data4 = url_list4[save].split(",")
            reader4.writerow(data4) 
        csvfile4.close()
        
    
def thread_run1():
    driver1.execute_script("window.scrollTo(0, document.body.scrollTop);")
    driver1.implicitly_wait(1)
    time.sleep(1)
    print("thread execute!")
        
    threading.Timer(15, thread_run1).start()  
    
def thread_run2():
    driver2.execute_script("window.scrollTo(0, document.body.scrollTop);")
    driver2.implicitly_wait(1)
    time.sleep(1)
    print("thread execute!")
        
    threading.Timer(15, thread_run2).start()
    
def thread_run3():
    driver3.execute_script("window.scrollTo(0, document.body.scrollTop);")
    driver3.implicitly_wait(1)
    time.sleep(1)
    print("thread execute!")
        
    threading.Timer(15, thread_run3).start()
    
def thread_run4():
    driver4.execute_script("window.scrollTo(0, document.body.scrollTop);")
    driver4.implicitly_wait(1)
    time.sleep(1)
    print("thread execute!")
        
    threading.Timer(15, thread_run4).start()

p1 = Process(target=main1)
p2 = Process(target=main2)
p3 = Process(target=main3)
p4 = Process(target=main4)
    
p1.start()
p2.start()
p3.start()
p4.start()
    
thread_run1()
thread_run2()
thread_run3()
thread_run4()

p1.join()
p2.join()
p3.join()
p4.join()

driver1.close()
driver2.close()
driver3.close()
driver4.close()

endTime = time.time() - startTime
print('끝났습니다. !! 걸린 시간은 : ',endTime) 
        